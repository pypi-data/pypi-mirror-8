from glob import glob
import os
import shutil

from .credential import Credential, CredentialNotFoundError
from .crypt import create_gpg, load_gpg

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


class Database(object):

    def __init__(self, path, gpg):
        self.path = path
        self.gpg = gpg

    @classmethod
    def create(cls, path, passphrase, gpg_bin="gpg"):
        gpg = create_gpg(gpg_bin, path, passphrase)
        return Database(path, gpg)

    @classmethod
    def from_path(cls, path, gpg_bin="gpg"):
        gpg = load_gpg(binary=gpg_bin, database_path=path)
        return Database(path, gpg)

    @property
    def gpg_key(self):
        return self.gpg.list_keys(secret=True)[0]["fingerprint"]

    @property
    def credentials(self):
        return [self.credential(os.path.basename(c))
                for c in glob(self.path + "/**")]

    def add(self, credential):
        encrypted_password = self.gpg.encrypt(
            credential.password,
            self.gpg_key,
            cipher_algo="AES256"
        )
        credential.password = str(encrypted_password)
        credential.save(database_path=self.path)

    def remove(self, name):
        credential_path = os.path.join(self.path, name)
        shutil.rmtree(credential_path)

    def edit(self, name, values):
        credential = self.credential(name)
        new_credential = Credential(
            name=values.get("name", credential.name),
            login=values.get("login", credential.login),
            password=values.get("password", credential.password),
            comments=values.get("comments", credential.comments),
        )
        self.remove(name=name)
        self.add(new_credential)

    def credential(self, name):
        credential_path = os.path.join(self.path, name)
        try:
            credential = Credential.from_path(credential_path)
        except FileNotFoundError:
            raise CredentialNotFoundError(
                "Credential was not found in the database")
        return credential

    def search(self, query):
        return [c for c in self.credentials
                if (query in c.name) or
                (query in c.login) or
                (query in c.comments)]
