import sqlite3
from .db_manager import DBManager

SCHEMA = """
CREATE TABLE projects (
    name CHAR(64) NOT NULL,
    description VARCHAR(1024),
    PRIMARY KEY(name)
);

CREATE TABLE documents (
    name CHAR(64) NOT NULL,
    project CHAR(64) NOT NULL,
    description VARCHAR(1024),
    created DATETIME NOT NULL,
    FOREIGN KEY (project) REFERENCES projects (name)
);

CREATE TABLE revisions (
    document INTEGER UNSIGNED NOT NULL,
    path VARCHAR(1024) NOT NULL,
    created DATETIME NOT NULL,
    revision CHAR(64) NOT NULL,
    latest BOOLEAN DEFAULT 0,
    FOREIGN KEY (document) REFERENCES documents (rowid)
);

CREATE TABLE tags (
    document INTEGER UNSIGNED NOT NULL,
    tag CHAR(64) NOT NULL,
    FOREIGN KEY (document) REFERENCES documents (rowid),
    PRIMARY KEY (document, tag)
);"""


class DBConnection:

    def __init__(self, dbpath: str):
        self.conn = sqlite3.connect(dbpath)
        self.conn.row_factory = sqlite3.Row

    def commit(self):
        self.conn.commit()

    def create_database(self):
        cursor = self.get_cursor()
        cursor.executescript(SCHEMA)
        cursor.close()

    def get_cursor(self) -> sqlite3.Cursor:
        return self.conn.cursor()

    def __enter__(self) -> DBManager:
        self._manager = DBManager(self.get_cursor())
        return self._manager

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._manager.close()
        self.commit()
