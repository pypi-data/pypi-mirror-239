import duckdb


from .credentials import Credentials
from .storage import Storage


class Connection:
    # cache of connections
    connections = {}
    httpfs = False

    @staticmethod
    def use(alias: str = "default") -> "Connection":
        if alias.strip() == "":
            alias = "default"

        if alias in Connection.connections:
            return Connection.connections[alias]

        raise Exception("Connection {} not found".format(alias))

    @staticmethod
    def connect(alias: str = "default",
             access_key: str = None,
             secret_key: str = None,
             session_token: str = None,
             region: str = "us-east-1",
             bucket: str = None,
             endpoint: str = None) -> "Connection":
        credentials = Credentials(access_key, secret_key, session_token)
        storage = Storage(credentials, region, bucket, endpoint)
        connection = Connection(storage, alias)
        return connection

    def __new__(cls, storage: Storage, alias: str = "default"):
        if alias.strip() == "":
            alias = "default"

        if alias in cls.connections:
            # use existing connection
            return cls.connections[alias]
        else:
            return super().__new__(cls)

    def __init__(self, storage: Storage, alias: str = "default"):
        self.setup()
        if alias.strip() == "":
            alias = "default"
        self.alias = alias
        self.storage = storage
        Connection.connections[self.alias] = self

    def setup(self):
        # only run once per process
        if not Connection.httpfs:
            duckdb.install_extension("httpfs")
            duckdb.load_extension("httpfs")
            Connection.httpfs = True

    def format(self, file_path: str):
        return self.storage.use(file_path)
