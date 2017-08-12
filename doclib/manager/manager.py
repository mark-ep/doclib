import os
import shutil
from typing import List

from .models import ProjectInfo, CategoryInfo, DocumentInfo
from .errors import ProjectError, CategoryError, DocumentError

class Manager:
    LIBDIR = os.path.expanduser("~/.doclib")

    @classmethod
    def get_projects(cls) -> List[ProjectInfo]:
        """
        get list of all the projects in the library
        """
        project_paths = [
            os.path.join(cls.LIBDIR, name) for name in os.listdir(cls.LIBDIR)
                if os.path.isdir(os.path.join(cls.LIBDIR, name))
        ]
        return [ProjectInfo.from_path(path) for path in project_paths]

    @classmethod
    def get_categories(cls, project_name: str) -> List[CategoryInfo]:
        """
        get list of all the categories of a project
        """
        project = cls.get_project(project_name)
        catpaths = [os.path.join(project.path, catname) for catname
                        in project.get_categories()]
        return [CategoryInfo.from_path(catpath) for catpath in catpaths]

    @classmethod
    def get_documents(cls, project_name: str, category_name: str) -> List[DocumentInfo]:
        """
        get list of all the documents in a category
        """
        category = cls.get_category(project_name, category_name)
        docpaths = [os.path.join(category.path, docname) for docname
                        in category.get_documents()]
        return [DocumentInfo.from_path(docpath) for docpath in docpaths]

    @classmethod
    def get_project(cls, project_name: str) -> ProjectInfo:
        """
        get a project
        """
        project_path = os.path.join(cls.LIBDIR, project_name)
        if not os.path.exists(project_path):
            raise ProjectError("no such project: %s" % project_name)
        return ProjectInfo.from_path(project_path)

    @classmethod
    def get_category(cls, project_name: str, category_name: str) -> CategoryInfo:
        """
        get a category
        """
        project = cls.get_project(project_name)
        category_path = os.path.join(project.path, category_name)
        if not os.path.exists(category_path):
            raise CategoryError("no such category: %s" % category_name)
        return CategoryInfo.from_path(category_path)

    @classmethod
    def get_document(cls, project_name: str, category_name: str,
                     document_name: str) -> DocumentInfo:
        """
        get a document
        """
        category = cls.get_category(project_name, category_name)
        document_path = os.path.join(category.path, document_name)
        if not os.path.exists(document_path):
            raise DocumentError("no such document: %s" % document_name)
        return DocumentInfo.from_path(document_path)

    @classmethod
    def add_project(cls, project_name: str):
        """
        add a new project to the library
        """
        project_path = os.path.join(cls.LIBDIR, project_name)
        if os.path.exists(project_path):
            raise ProjectError("project already exists: %s" % project_name)
        os.mkdir(project_path)
        return cls.get_project(project_name)

    @classmethod
    def add_category(cls, project_name: str, category_name: str):
        """
        add a new category to the library
        """
        project = cls.get_project(project_name)
        category_path =\
            os.path.join(project.path, category_name)
        if os.path.exists(category_path):
            raise CategoryError("category already exists: %s" % category_name)
        os.mkdir(category_path)
        return cls.get_category(project_name, category_name)

    @classmethod
    def add_document(cls, project_name: str, category_name: str,
                     document: DocumentInfo, clobber: bool=False):
        """
        add a new document to the library
        """
        category = cls.get_category(project_name, category_name)
        document_path =\
            os.path.join(category.path, document.name)
        if os.path.exists(document_path) and not clobber:
            raise DocumentError("document already exists: %s" % document.name)
        if not os.path.exists(document.path):
            raise DocumentError("document does not exist: %s" % document.path)
        shutil.copyfile(document.path, document_path)

    @classmethod
    def remove_project(cls, project_name: str, recursive: bool=False):
        """
        delete a project
        """
        project = cls.get_project(project_name)
        if project.get_categories() and not recursive:
            raise ProjectError("project is not empty: %s" % project_name)
        shutil.rmtree(project.path)

    @classmethod
    def remove_category(cls, project_name: str, category_name: str,
                        recursive: bool=False):
        """
        delete a category
        """
        category = cls.get_category(project_name, category_name)
        if category.get_documents() and not recursive:
            raise CategoryError("category is not empty: %s" % category_name)
        shutil.rmtree(category.path)

    @classmethod
    def remove_document(cls, project_name: str, category_name: str,
                        document_name: str):
        """
        delete a document
        """
        document = cls.get_document(project_name, category_name, document_name)
        os.remove(document.path)
