import os


class CredentialNotFoundError(ValueError):
    pass


class Credential(object):
    def __init__(self, name, login, password, comments):
        self.name = name
        self.login = login
        self.password = password
        self.comments = comments

    def save(self, database_path):
        credential_path = os.path.join(database_path, self.name)
        os.makedirs(credential_path)

        with open(os.path.join(credential_path, "login"), "w") as f:
            f.write(self.login)

        with open(os.path.join(credential_path, "password"), "w") as f:
            f.write(self.password)

        with open(os.path.join(credential_path, "comments"), "w") as f:
            f.write(self.comments)

    @classmethod
    def from_path(cls, path):
        return Credential(
            name=os.path.basename(path),
            login=open(os.path.join(path, "login")).read(),
            password=open(os.path.join(path, "password")).read(),
            comments=open(os.path.join(path, "comments")).read()
        )

    def __str__(self):
        return "Credential(name={}, login={})".format(
            self.name,
            self.login
        )
