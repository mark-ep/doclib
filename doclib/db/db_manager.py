import sqlite3


class DBManager:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def close(self):
        self.cursor.close()

    def _get_document_id(self, project: str, document: str):
        query = self.cursor.execute(
            "SELECT rowid FROM documents d "
            "WHERE d.name=:doc AND d.project=:project",
            dict(doc=document, project=project)
        )
        docid, = query.fetchone()
        return docid

    def get_projects(self):
        return self.cursor.execute('SELECT * FROM projects').fetchall()

    def add_project(self, name: str, description: str=None):
        self.cursor.execute(
            'INSERT INTO projects (name, description) VALUES (:name, :desc)',
            dict(name=name, desc=description)
        )

    def get_project(self, name: str):
        self.cursor.execute(
            'SELECT * FROM projects WHERE name=:name', dict(name=name)
        )
        return self.cursor.fetchone()

    def rename_project(self, name: str, new_name: str):
        self.cursor.execute(
            'UPDATE projects SET (name) VALUES (:new_name) WHERE name=:name',
            dict(name=name, new_name=new_name)
        )

    def delete_project(self, name: str):
        self.cursor.execute(
            'DELETE FROM projects WHERE name=:name',
            dict(name=name)
        )

    def get_documents(self, project: str):
        return self.cursor.execute(
            'SELECT * FROM documents WHERE project=:project',
            dict(project=project)
        ).fetchall()

    def get_document(self, project: str, document: str):
        self.cursor.execute(
            'SELECT * FROM documents WHERE project=:project AND name=:doc',
            dict(project=project, doc=document)
        )
        return self.cursor.fetchone()

    def add_document(self, project: str, document: str, description: str,
                     *tags: str):
        self.cursor.execute(
            "INSERT INTO documents (name, project, description, date) "
            "VALUES (:name, :project, :desc, DATETIME('now'))",
            dict(name=document, project=project, desc=description, date=date)
        )
        if tags:
            self.tag_document(project, document, tags)

    def delete_document(self, project: str, document: str):
        self.cursor.execute(
            'DELETE FROM documents WHERE name=:name AND project=:project',
            dict(name=document, project=project)
        )

    def rename_document(self, project: str, document: str, new_name: str,
                        new_project: str):
        self.cursor.execute(
            "UPDATE documents SET (name, project) VALUES (:new_name, :new_project)"
            "WHERE name=:name AND project=:project",
            dict(name=document, project=project, new_name=new_name,
                 new_project=new_project)
        )

    def tag_document(self, project: str, document: str, *tags: str):
        # get id of document
        docid = self._get_document_id(project, document)

        rows = [dict(docid=docid, tag=tag) for tag in tags]
        self.cursor.executemany(
            "INSERT INTO tags (document, tag) VALUES (:docid, :tag)", rows
        )

    def get_revisions(self, project: str, document: str):
        return self.cursor.execute(
            "SELECT * FROM revisions r "
            "JOIN documents d ON r.document=d.rowid "
            "WHERE d.name=:document AND d.project=:project",
            dict(document=document, project=project)
        ).fetchall()

    def get_revision(self, project: str, document: str, revision: str):
        return self.cursor.execute(
            "SELECT * FROM revisions r "
            "JOIN documents d ON r.document=d.rowid "
            "WHERE d.name=:document AND d.project=:project AND r.revision=:rev",
            dict(document=document, project=project, rev=revision)
        ).fetchone()

    def add_revision(self, project: str, document: str, path: str, revision: str,
                     latest: bool):
        docid = self._get_document_id(project, document)
        self.cursor.execute(
            "INSERT INTO revisions (document, path, revision, created, latest) "
            "VALUES (:docid, :path, :rev, DATETIME('now'), :latest)",
            dict(docid=docid, path=path, rev=revision, latest=latest)
        )

    def tag_search(self, *tags: str):
        placeholders = ', '.join(':tag%i' % i for i, _ in enumerate(tags))
        values = {'tag%i' % i: tag for i, tag in enumerate(tags)}
        values['len'] = len(tags)

        return self.cursor.execute(
            "SELECT d.* "
            "FROM documents d, tags t "
            "WHERE d.rowid=t.document "
            "AND t.tag IN (%s) "
            "GROUP BY d.rowid "
            "HAVING COUNT (d.rowid)=:len" % placeholders,
            values
        ).fetchall()

    def get_tags(self):
        return self.cursor.execute(
            "SELECT * FROM tags t GROUP BY t.tag"
        ).fetchall()
