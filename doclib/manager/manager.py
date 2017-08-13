import os
import shutil
from typing import List

from doclib.db import DBConnection
from doclib.const import DocumentMode

class Manager:
    LIBDIR = os.path.expanduser("~/.doclib")
    DBPATH = os.path.expanduser("library.db")

    @classmethod
    def get_projects(cls):
        with DBConnection(cls.DBPATH) as db:
            projects = db.get_projects()
        return projects

    @classmethod
    def get_project(cls, project_name: str):
        """
        get a project
        """
        with DBConnection(cls.DBPATH) as db:
            project = db.get_project(project_name)
        return project

    @classmethod
    def add_project(cls, project_name: str, desc: str=None):
        with DBConnection(cls.DBPATH) as db:
            db.add_project(project_name, desc)
        project_path = os.path.join(cls.LIBDIR, project_name)
        if not os.path.exists(project_path):
            os.mkdir(project_path)

    @classmethod
    def remove_project(cls, project_name: str, force: bool=False):
        pass

    @classmethod
    def move_project(cls, project_name: str, new_name: str):
        pass

    @classmethod
    def copy_project(cls, project_name: str, new_name: str):
        pass

    # DOCUMENTS

    @classmethod
    def get_documents(cls, project_name: str):
        with DBConnection(cls.DBPATH) as db:
            docs = db.get_documents(project_name)
        return docs

    @classmethod
    def get_document(cls, project_name: str, document_name: str):
        with DBConnection(cls.DBPATH) as db:
            doc = db.get_document(project_name, document_name)
        return doc

    @classmethod
    def add_document(cls, project_name: str, document_name: str,
                     document_path: str, mode: DocumentMode=DocumentMode.move,
                     revision: str=None, latest: bool=True, #TODO: description?
                     *tags: str):
        # create document if needed
        if mode == DocumentMode.copy:
            basename = os.path.basename(path)
            newpath = os.path.join(
                cls.LIBDIR, project_name, document_name, basename
            )
            shutil.copyfile(path, newpath)
            path = newpath
        if mode == DocumentMode.move:
            basename = os.path.basename(path)
            newpath = os.path.join(
                cls.LIBDIR, project_name, document_name, basename
            )
            shutil.copyfile(path, newpath) #TODO: move instead
            path = newpath
        with DBConnection(cls.DBPATH) as db:
            db.add_revision(project_name, document_name, path, revision, latest)
        if tags:
            db.tag_document(project, document, tags)

    @classmethod
    def remove_document(cls, project_name: str, document_name: str,
                        force: bool=False, revision: str=None):
        shutil.rmtree(project.path)
        pass

    @classmethod
    def move_document(cls, project_name: str, document_name: str,
                        new_name: str=None, new_project: str=None):
        pass

    @classmethod
    def copy_document(cls, project_name: str, document_name: str,
                        new_name: str=None, new_project: str=None):
        pass

    @classmethod
    def open_document(cls, project_name: str, document_name: str,
                        revision: str=None):
        pass

    @classmethod
    def tag_document(cls, project_name: str, document_name: str, *tags: str):
        pass

    @classmethod
    def set_latest_revision(cls, project_name: str, document_name: str,
                            revision: str):
        pass

    # tags

    @classmethod
    def list_tags(cls):
        with DBConnection(cls.DBPATH) as db:
            return db.get_tags()

    @classmethod
    def remove_tags(cls, *tags: str):
        pass

    @classmethod
    def search_tags(cls, *tags: str):
        with DBConnection(cls.DBPATH) as db:
            return db.tag_search(*tags)
