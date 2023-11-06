import re
from .connection import Connection

def replace_connection_aliases(query: str, replacer):
    """
    Find the placeholders for connections and replace the aliases within the query.
    ex. SELECT * FROM $$s3:/path/to/file.csv

    ex. SELECT * FROM $$s3:/path/to/file.csv T1 WHERE T1.col1 = 1

    ex. SELECT * FROM $$:/path/to/file.csv T1 WHERE T1.col1 = 1

    ex. SELECT * FROM $$s3:/path/to/file.csv T1
        JOIN $$:/path/to/file.csv T2 ON T2.id = T1.col_id
        WHERE T1.col_id = 1
        UNION
        SELECT * FROM $$s3:/path/to/file.csv T1
        JOIN $$:/path/to/file.csv T2 ON T2.id = T1.col_id
        WHERE T1.col_id > 100
    """
    query = query.strip()

    # Find Regex matches of aliases and the file paths following them:
    matches = re.findall(r"\$\$([a-zA-Z0-9_-]*):([^\n\r\s]+|$)", query)

    # Create a mapping of the aliases to the file paths:
    mapping = {}

    # Replace the aliases with the file paths:
    # ex. SELECT * FROM $$s3:/path/to/file.csv
    #
    # connection = "s3://mybucket/{path}?s3_endpoint=http://localhost:9000"
    #
    # alias = "s3"
    # file_path = "/path/to/file.csv"
    #
    # query = query.replace(f"$${alias}:{file_path}", replacer(alias, file_path))
    #
    # becomes: SELECT * FROM s3://mybucket/path/to/file.csv?endpoint=http://localhost:9000
    for match in matches:
        alias, file_path = match
        file_path = file_path.strip()
        key = f"$${alias}:{file_path}"

        mapping[key] = replacer(alias, file_path)
        query = query.replace(key, mapping[key])

    return query, mapping

def qualify_connections(alias: str, file_path: str):
    return Connection.use(alias).format(file_path)


class SQL:
    def __init__(self, query: str):
        if not isinstance(query, str):
            raise TypeError(f"Expected str, got {type(query)}")
        if not query or query.strip() == "":
            raise ValueError("Query cannot be empty")

        self.raw = query
        query, mapping = replace_connection_aliases(query, qualify_connections)
        self.query = query
        self.mapping = mapping
        print({ "raw": self.raw, "query": self.query, "mapping": self.mapping })

    def __repr__(self):
        return f"Sql({self.query!r})"

    def __str__(self):
        return f"{self.query!s}"

    def __eq__(self, other):
        if isinstance(other, Query):
            return self.query == other.query
        return NotImplemented

    def __hash__(self):
        return hash(self.query)
