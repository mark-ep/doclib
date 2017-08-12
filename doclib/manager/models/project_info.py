import os
from typing import List


class ProjectInfo:
    @property
    def name(self) -> str:
        """
        the name of the project
        """
        return self._name

    @property
    def path(self) -> str:
        """
        the path of the project
        """
        return self._path

    def get_categories(self) -> List[str]:
        """
        categories in the project
        """
        return self._categories

    def __init__(self, name: str, path: str=None, *docs: str):
        self._name = name
        self._path = path
        self._categories = docs

    @classmethod
    def from_path(cls, path: str) -> "ProjectInfo":
        _, name = os.path.split(path)
        categories = [p for p in os.listdir(path) if os.path.isdir(p)]
        return cls(name=name, path=path, *categories)
