# -*- coding: utf-8 -*-
# secrets.py
# Copyright (C) 2014 LEAP
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""
Soledad secrets handling.
"""


import os
import scrypt
import hmac
import logging
import binascii
import errno


from hashlib import sha256
import simplejson as json


from leap.soledad.common import (
    soledad_assert,
    soledad_assert_type
)
from leap.soledad.common.document import SoledadDocument
from leap.soledad.common.crypto import (
    MacMethods,
    UnknownMacMethod,
    WrongMac,
    MAC_KEY,
    MAC_METHOD_KEY,
)
from leap.soledad.common.errors import (
    InvalidTokenError,
    NotLockedError,
    AlreadyLockedError,
    LockTimedOutError,
)
from leap.soledad.client.events import (
    SOLEDAD_CREATING_KEYS,
    SOLEDAD_DONE_CREATING_KEYS,
    SOLEDAD_DOWNLOADING_KEYS,
    SOLEDAD_DONE_DOWNLOADING_KEYS,
    SOLEDAD_UPLOADING_KEYS,
    SOLEDAD_DONE_UPLOADING_KEYS,
    signal,
)


logger = logging.getLogger(name=__name__)


#
# Exceptions
#


class SecretsException(Exception):
    """
    Generic exception type raised by this module.
    """


class NoStorageSecret(SecretsException):
    """
    Raised when trying to use a storage secret but none is available.
    """
    pass


class PassphraseTooShort(SecretsException):
    """
    Raised when trying to change the passphrase but the provided passphrase is
    too short.
    """


class BootstrapSequenceError(SecretsException):
    """
    Raised when an attempt to generate a secret and store it in a recovery
    document on server failed.
    """


#
# Secrets handler
#

class SoledadSecrets(object):
    """
    Soledad secrets handler.

    The first C{self.REMOTE_STORAGE_SECRET_LENGTH} bytes of the storage
    secret are used for remote storage encryption. We use the next
    C{self.LOCAL_STORAGE_SECRET} bytes to derive a key for local storage.
    From these bytes, the first C{self.SALT_LENGTH} bytes are used as the
    salt and the rest as the password for the scrypt hashing.
    """

    LOCAL_STORAGE_SECRET_LENGTH = 512
    """
    The length, in bytes, of the secret used to derive a passphrase for the
    SQLCipher database.
    """

    REMOTE_STORAGE_SECRET_LENGTH = 512
    """
    The length, in bytes, of the secret used to derive an encryption key and a
    MAC auth key for remote storage.
    """

    SALT_LENGTH = 64
    """
    The length, in bytes, of the salt used to derive the key for the storage
    secret encryption.
    """

    GEN_SECRET_LENGTH = LOCAL_STORAGE_SECRET_LENGTH \
        + REMOTE_STORAGE_SECRET_LENGTH \
        + SALT_LENGTH  # for sync db
    """
    The length, in bytes, of the secret to be generated. This includes local
    and remote secrets, and the salt for deriving the sync db secret.
    """

    MINIMUM_PASSPHRASE_LENGTH = 6
    """
    The minimum length, in bytes, for a passphrase. The passphrase length is
    only checked when the user changes her passphrase, not when she
    instantiates Soledad.
    """

    IV_SEPARATOR = ":"
    """
    A separator used for storing the encryption initial value prepended to the
    ciphertext.
    """

    UUID_KEY = 'uuid'
    STORAGE_SECRETS_KEY = 'storage_secrets'
    SECRET_KEY = 'secret'
    CIPHER_KEY = 'cipher'
    LENGTH_KEY = 'length'
    KDF_KEY = 'kdf'
    KDF_SALT_KEY = 'kdf_salt'
    KDF_LENGTH_KEY = 'kdf_length'
    KDF_SCRYPT = 'scrypt'
    CIPHER_AES256 = 'aes256'
    """
    Keys used to access storage secrets in recovery documents.
    """

    def __init__(self, uuid, passphrase, secrets_path, shared_db, crypto,
                 secret_id=None):
        """
        Initialize the secrets manager.

        :param uuid: User's unique id.
        :type uuid: str
        :param passphrase: The passphrase for locking and unlocking encryption
                           secrets for local and remote storage.
        :type passphrase: unicode
        :param secrets_path: Path for storing encrypted key used for
                             symmetric encryption.
        :type secrets_path: str
        :param shared_db: The shared database that stores user secrets.
        :type shared_db: leap.soledad.client.shared_db.SoledadSharedDatabase
        :param crypto: A soledad crypto object.
        :type crypto: SoledadCrypto
        :param secret_id: The id of the storage secret to be used.
        :type secret_id: str
        """
        self._uuid = uuid
        self._passphrase = passphrase
        self._secrets_path = secrets_path
        self._shared_db = shared_db
        self._crypto = crypto
        self._secret_id = secret_id
        self._secrets = {}

    def bootstrap(self):
        """
        Bootstrap secrets.

        Soledad secrets bootstrap is the following sequence of stages:

        * stage 1 - local secret loading:
            - if secrets exist locally, load them.
        * stage 2 - remote secret loading:
            - else, if secrets exist in server, download them.
        * stage 3 - secret generation:
            - else, generate a new secret and store in server.

        This method decides which bootstrap stages have already been performed
        and performs the missing ones in order.

        :raise BootstrapSequenceError: Raised when the secret generation and
            storage on server sequence has failed for some reason.
        """
        # STAGE 1 - verify if secrets exist locally
        if not self._has_secret():  # try to load from local storage.

            # STAGE 2 - there are no secrets in local storage, so try to fetch
            # encrypted secrets from server.
            logger.info(
                'Trying to fetch cryptographic secrets from shared recovery '
                'database...')

            # --- start of atomic operation in shared db ---

            # obtain lock on shared db
            token = timeout = None
            try:
                token, timeout = self._shared_db.lock()
            except AlreadyLockedError:
                raise BootstrapSequenceError('Database is already locked.')
            except LockTimedOutError:
                raise BootstrapSequenceError('Lock operation timed out.')

            self._get_or_gen_crypto_secrets()

            # release the lock on shared db
            try:
                self._shared_db.unlock(token)
                self._shared_db.close()
            except NotLockedError:
                # for some reason the lock expired. Despite that, secret
                # loading or generation/storage must have been executed
                # successfully, so we pass.
                pass
            except InvalidTokenError:
                # here, our lock has not only expired but also some other
                # client application has obtained a new lock and is currently
                # doing its thing in the shared database. Using the same
                # reasoning as above, we assume everything went smooth and
                # pass.
                pass
            except Exception as e:
                logger.error("Unhandled exception when unlocking shared "
                             "database.")
                logger.exception(e)

            # --- end of atomic operation in shared db ---

    def _has_secret(self):
        """
        Return whether there is a storage secret available for use or not.

        :return: Whether there's a storage secret for symmetric encryption.
        :rtype: bool
        """
        if self._secret_id is None or self._secret_id not in self._secrets:
            try:
                self._load_secrets()  # try to load from disk
            except IOError as e:
                logger.warning('IOError while loading secrets from disk: %s' % str(e))
                return False
        return self.storage_secret is not None

    def _load_secrets(self):
        """
        Load storage secrets from local file.
        """
        # does the file exist in disk?
        if not os.path.isfile(self._secrets_path):
            raise IOError('File does not exist: %s' % self._secrets_path)
        # read storage secrets from file
        content = None
        with open(self._secrets_path, 'r') as f:
            content = json.loads(f.read())
        _, mac = self._import_recovery_document(content)
        # choose first secret if no secret_id was given
        if self._secret_id is None:
            self.set_secret_id(self._secrets.items()[0][0])
        # enlarge secret if needed
        enlarged = False
        if len(self._secrets[self._secret_id]) < self.GEN_SECRET_LENGTH:
            gen_len = self.GEN_SECRET_LENGTH \
                - len(self._secrets[self._secret_id])
            new_piece = os.urandom(gen_len)
            self._secrets[self._secret_id] += new_piece
            enlarged = True
        # store and save in shared db if needed
        if not mac or enlarged:
            self._store_secrets()
            self._put_secrets_in_shared_db()

    def _get_or_gen_crypto_secrets(self):
        """
        Retrieves or generates the crypto secrets.

        :raises BootstrapSequenceError: Raised when unable to store secrets in
                                        shared database.
        """
        doc = self._get_secrets_from_shared_db()

        if doc:
            logger.info(
                'Found cryptographic secrets in shared recovery '
                'database.')
            _, mac = self._import_recovery_document(doc.content)
            if mac is False:
                self.put_secrets_in_shared_db()
            self._store_secrets()  # save new secrets in local file
            if self._secret_id is None:
                self.set_secret_id(self._secrets.items()[0][0])
        else:
            # STAGE 3 - there are no secrets in server also, so
            # generate a secret and store it in remote db.
            logger.info(
                'No cryptographic secrets found, creating new '
                ' secrets...')
            self.set_secret_id(self._gen_secret())
            try:
                self._put_secrets_in_shared_db()
            except Exception as ex:
                # storing generated secret in shared db failed for
                # some reason, so we erase the generated secret and
                # raise.
                try:
                    os.unlink(self._secrets_path)
                except OSError as e:
                    if e.errno != errno.ENOENT:  # no such file or directory
                        logger.exception(e)
                logger.exception(ex)
                raise BootstrapSequenceError(
                    'Could not store generated secret in the shared '
                    'database, bailing out...')

    #
    # Shared DB related methods
    #

    def _shared_db_doc_id(self):
        """
        Calculate the doc_id of the document in the shared db that stores key
        material.

        :return: the hash
        :rtype: str
        """
        return sha256(
            '%s%s' %
            (self._passphrase_as_string(), self._uuid)).hexdigest()

    def _export_recovery_document(self):
        """
        Export the storage secrets.

        A recovery document has the following structure:

            {
                'storage_secrets': {
                    '<storage_secret id>': {
                        'kdf': 'scrypt',
                        'kdf_salt': '<b64 repr of salt>'
                        'kdf_length': <key length>
                        'cipher': 'aes256',
                        'length': <secret length>,
                        'secret': '<encrypted storage_secret>',
                    },
                },
                'kdf': 'scrypt',
                'kdf_salt': '<b64 repr of salt>',
                'kdf_length: <key length>,
                '_mac_method': 'hmac',
                '_mac': '<mac>'
            }

        Note that multiple storage secrets might be stored in one recovery
        document. This method will also calculate a MAC of a string
        representation of the secrets dictionary.

        :return: The recovery document.
        :rtype: dict
        """
        # create salt and key for calculating MAC
        salt = os.urandom(self.SALT_LENGTH)
        key = scrypt.hash(self._passphrase_as_string(), salt, buflen=32)
        # encrypt secrets
        encrypted_secrets = {}
        for secret_id in self._secrets:
            encrypted_secrets[secret_id] = self._encrypt_storage_secret(
                self._secrets[secret_id])
        # create the recovery document
        data = {
            self.STORAGE_SECRETS_KEY: encrypted_secrets,
            self.KDF_KEY: self.KDF_SCRYPT,
            self.KDF_SALT_KEY: binascii.b2a_base64(salt),
            self.KDF_LENGTH_KEY: len(key),
            MAC_METHOD_KEY: MacMethods.HMAC,
            MAC_KEY: hmac.new(
                key,
                json.dumps(encrypted_secrets),
                sha256).hexdigest(),
        }
        return data

    def _import_recovery_document(self, data):
        """
        Import storage secrets for symmetric encryption and uuid (if present)
        from a recovery document.

        Note that this method does not store the imported data on disk. For
        that, use C{self._store_secrets()}.

        :param data: The recovery document.
        :type data: dict

        :return: A tuple containing the number of imported secrets and whether
                 there was MAC informationa available for authenticating.
        :rtype: (int, bool)
        """
        soledad_assert(self.STORAGE_SECRETS_KEY in data)
        # check mac of the recovery document
        mac = None
        if MAC_KEY in data:
            soledad_assert(data[MAC_KEY] is not None)
            soledad_assert(MAC_METHOD_KEY in data)
            soledad_assert(self.KDF_KEY in data)
            soledad_assert(self.KDF_SALT_KEY in data)
            soledad_assert(self.KDF_LENGTH_KEY in data)
            if data[MAC_METHOD_KEY] == MacMethods.HMAC:
                key = scrypt.hash(
                    self._passphrase_as_string(),
                    binascii.a2b_base64(data[self.KDF_SALT_KEY]),
                    buflen=32)
                mac = hmac.new(
                    key,
                    json.dumps(data[self.STORAGE_SECRETS_KEY]),
                    sha256).hexdigest()
            else:
                raise UnknownMacMethod('Unknown MAC method: %s.' %
                                       data[MAC_METHOD_KEY])
            if mac != data[MAC_KEY]:
                raise WrongMac('Could not authenticate recovery document\'s '
                               'contents.')
        # include secrets in the secret pool.
        secret_count = 0
        for secret_id, encrypted_secret in data[self.STORAGE_SECRETS_KEY].items():
            if secret_id not in self._secrets:
                try:
                    self._secrets[secret_id] = \
                        self._decrypt_storage_secret(encrypted_secret)
                    secret_count += 1
                except SecretsException as e:
                    logger.error("Failed to decrypt storage secret: %s"
                                 % str(e))
        return secret_count, mac

    def _get_secrets_from_shared_db(self):
        """
        Retrieve the document with encrypted key material from the shared
        database.

        :return: a document with encrypted key material in its contents
        :rtype: SoledadDocument
        """
        signal(SOLEDAD_DOWNLOADING_KEYS, self._uuid)
        db = self._shared_db
        if not db:
            logger.warning('No shared db found')
            return
        doc = db.get_doc(self._shared_db_doc_id())
        signal(SOLEDAD_DONE_DOWNLOADING_KEYS, self._uuid)
        return doc

    def _put_secrets_in_shared_db(self):
        """
        Assert local keys are the same as shared db's ones.

        Try to fetch keys from shared recovery database. If they already exist
        in the remote db, assert that that data is the same as local data.
        Otherwise, upload keys to shared recovery database.
        """
        soledad_assert(
            self._has_secret(),
            'Tried to send keys to server but they don\'t exist in local '
            'storage.')
        # try to get secrets doc from server, otherwise create it
        doc = self._get_secrets_from_shared_db()
        if doc is None:
            doc = SoledadDocument(
                doc_id=self._shared_db_doc_id())
        # fill doc with encrypted secrets
        doc.content = self._export_recovery_document()
        # upload secrets to server
        signal(SOLEDAD_UPLOADING_KEYS, self._uuid)
        db = self._shared_db
        if not db:
            logger.warning('No shared db found')
            return
        db.put_doc(doc)
        signal(SOLEDAD_DONE_UPLOADING_KEYS, self._uuid)

    #
    # Management of secret for symmetric encryption.
    #

    def _decrypt_storage_secret(self, encrypted_secret_dict):
        """
        Decrypt the storage secret.

        Storage secret is encrypted before being stored. This method decrypts
        and returns the decrypted storage secret.

        :param encrypted_secret_dict: The encrypted storage secret.
        :type encrypted_secret_dict:  dict

        :return: The decrypted storage secret.
        :rtype: str

        :raise SecretsException: Raised in case the decryption of the storage
                                 secret fails for some reason.
        """
        # calculate the encryption key
        if encrypted_secret_dict[self.KDF_KEY] != self.KDF_SCRYPT:
            raise SecretsException("Unknown KDF in stored secret.")
        key = scrypt.hash(
            self._passphrase_as_string(),
            # the salt is stored base64 encoded
            binascii.a2b_base64(
                encrypted_secret_dict[self.KDF_SALT_KEY]),
            buflen=32,  # we need a key with 256 bits (32 bytes).
        )
        if encrypted_secret_dict[self.KDF_LENGTH_KEY] != len(key):
            raise SecretsException("Wrong length of decryption key.")
        if encrypted_secret_dict[self.CIPHER_KEY] != self.CIPHER_AES256:
            raise SecretsException("Unknown cipher in stored secret.")
        # recover the initial value and ciphertext
        iv, ciphertext = encrypted_secret_dict[self.SECRET_KEY].split(
            self.IV_SEPARATOR, 1)
        ciphertext = binascii.a2b_base64(ciphertext)
        decrypted_secret = self._crypto.decrypt_sym(ciphertext, key, iv=iv)
        if encrypted_secret_dict[self.LENGTH_KEY] != len(decrypted_secret):
            raise SecretsException("Wrong length of decrypted secret.")
        return decrypted_secret

    def _encrypt_storage_secret(self, decrypted_secret):
        """
        Encrypt the storage secret.

        An encrypted secret has the following structure:

            {
                '<secret_id>': {
                        'kdf': 'scrypt',
                        'kdf_salt': '<b64 repr of salt>'
                        'kdf_length': <key length>
                        'cipher': 'aes256',
                        'length': <secret length>,
                        'secret': '<encrypted b64 repr of storage_secret>',
                }
            }

        :param decrypted_secret: The decrypted storage secret.
        :type decrypted_secret: str

        :return: The encrypted storage secret.
        :rtype: dict
        """
        # generate random salt
        salt = os.urandom(self.SALT_LENGTH)
        # get a 256-bit key
        key = scrypt.hash(self._passphrase_as_string(), salt, buflen=32)
        iv, ciphertext = self._crypto.encrypt_sym(decrypted_secret, key)
        encrypted_secret_dict = {
            # leap.soledad.crypto submodule uses AES256 for symmetric
            # encryption.
            self.KDF_KEY: self.KDF_SCRYPT,
            self.KDF_SALT_KEY: binascii.b2a_base64(salt),
            self.KDF_LENGTH_KEY: len(key),
            self.CIPHER_KEY: self.CIPHER_AES256,
            self.LENGTH_KEY: len(decrypted_secret),
            self.SECRET_KEY: '%s%s%s' % (
                str(iv), self.IV_SEPARATOR, binascii.b2a_base64(ciphertext)),
        }
        return encrypted_secret_dict

    @property
    def storage_secret(self):
        """
        Return the storage secret.

        :return: The decrypted storage secret.
        :rtype: str
        """
        return self._secrets.get(self._secret_id)

    def set_secret_id(self, secret_id):
        """
        Define the id of the storage secret to be used.

        This method will also replace the secret in the crypto object.

        :param secret_id: The id of the storage secret to be used.
        :type secret_id: str
        """
        self._secret_id = secret_id

    def _gen_secret(self):
        """
        Generate a secret for symmetric encryption and store in a local
        encrypted file.

        This method emits the following signals:

            * SOLEDAD_CREATING_KEYS
            * SOLEDAD_DONE_CREATING_KEYS

        :return: The id of the generated secret.
        :rtype: str
        """
        signal(SOLEDAD_CREATING_KEYS, self._uuid)
        # generate random secret
        secret = os.urandom(self.GEN_SECRET_LENGTH)
        secret_id = sha256(secret).hexdigest()
        self._secrets[secret_id] = secret
        self._store_secrets()
        signal(SOLEDAD_DONE_CREATING_KEYS, self._uuid)
        return secret_id

    def _store_secrets(self):
        """
        Store secrets in C{Soledad.STORAGE_SECRETS_FILE_PATH}.
        """
        with open(self._secrets_path, 'w') as f:
            f.write(
                json.dumps(
                    self._export_recovery_document()))

    def change_passphrase(self, new_passphrase):
        """
        Change the passphrase that encrypts the storage secret.

        :param new_passphrase: The new passphrase.
        :type new_passphrase: unicode

        :raise NoStorageSecret: Raised if there's no storage secret available.
        """
        # TODO: maybe we want to add more checks to guarantee passphrase is
        # reasonable?
        soledad_assert_type(new_passphrase, unicode)
        if len(new_passphrase) < self.MINIMUM_PASSPHRASE_LENGTH:
            raise PassphraseTooShort(
                'Passphrase must be at least %d characters long!' %
                self.MINIMUM_PASSPHRASE_LENGTH)
        # ensure there's a secret for which the passphrase will be changed.
        if not self._has_secret():
            raise NoStorageSecret()
        self._passphrase = new_passphrase
        self._store_secrets()
        self._put_secrets_in_shared_db()

    #
    # Setters and getters
    #

    @property
    def secret_id(self):
        return self._secret_id

    def _get_secrets_path(self):
        return self._secrets_path

    def _set_secrets_path(self, secrets_path):
        self._secrets_path = secrets_path

    secrets_path = property(
         _get_secrets_path,
         _set_secrets_path,
        doc='The path for the file containing the encrypted symmetric secret.')

    @property
    def passphrase(self):
        """
        Return the passphrase for locking and unlocking encryption secrets for
        local and remote storage.
        """
        return self._passphrase

    def _passphrase_as_string(self):
        return self._passphrase.encode('utf-8')

    #
    # remote storage secret
    #

    @property
    def remote_storage_secret(self):
        """
        Return the secret for remote storage.
        """
        key_start = 0
        key_end =  self.REMOTE_STORAGE_SECRET_LENGTH
        return self.storage_secret[key_start:key_end]

    #
    # local storage key
    #

    def _get_local_storage_secret(self):
        """
        Return the local storage secret.

        :return: The local storage secret.
        :rtype: str
        """
        pwd_start = self.REMOTE_STORAGE_SECRET_LENGTH + self.SALT_LENGTH
        pwd_end = self.REMOTE_STORAGE_SECRET_LENGTH + self.LOCAL_STORAGE_SECRET_LENGTH
        return self.storage_secret[pwd_start:pwd_end]

    def _get_local_storage_salt(self):
        """
        Return the local storage salt.

        :return: The local storage salt.
        :rtype: str
        """
        salt_start = self.REMOTE_STORAGE_SECRET_LENGTH
        salt_end = salt_start + self.SALT_LENGTH
        return self.storage_secret[salt_start:salt_end]

    def get_local_storage_key(self):
        """
        Return the local storage key derived from the local storage secret.

        :return: The key for protecting the local database.
        :rtype: str
        """
        return scrypt.hash(
            password=self._get_local_storage_secret(),
            salt=self._get_local_storage_salt(),
            buflen=32,  # we need a key with 256 bits (32 bytes)
        )

   #
   # sync db key
   #

    def _get_sync_db_salt(self):
        """
        Return the salt for sync db.
        """
        salt_start = self.LOCAL_STORAGE_SECRET_LENGTH \
            + self.REMOTE_STORAGE_SECRET_LENGTH
        salt_end = salt_start + self.SALT_LENGTH
        return self.storage_secret[salt_start:salt_end]

    def get_sync_db_key(self):
        """
        Return the key for protecting the sync database.

        :return: The key for protecting the sync database.
        :rtype: str
        """
        return scrypt.hash(
            password=self._get_local_storage_secret(),
            salt=self._get_sync_db_salt(),
            buflen=32,  # we need a key with 256 bits (32 bytes)
        )
