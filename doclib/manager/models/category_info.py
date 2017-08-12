import os
from typing import List


class CategoryInfo:
    @property
    def name(self) -> str:
        """
        the name of the category
        """
        return self._name

    @property
    def path(self) -> str:
        """
        the path of the category
        """
        return self._path

    def get_documents(self) -> List[str]:
        """
        documents in the category
        """
        return self._documents

    def __init__(self, name: str, path: str=None, *docs: str):
        self._name = name
        self._path = path
        self._documents = docs

    @classmethod
    def from_path(cls, path: str) -> "CategoryInfo":
        _, name = os.path.split(path)
        docs = os.listdir(path)
        return cls(name=name, path=path, *docs)
