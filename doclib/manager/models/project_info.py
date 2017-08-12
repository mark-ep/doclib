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

    def __init__(self, name: str, path: str=None, *cats: str):
        self._name = name
        self._path = path
        self._categories = cats

    @classmethod
    def from_path(cls, path: str) -> "ProjectInfo":
        _, name = os.path.split(path)
        categories = [p for p in os.listdir(path)
                        if os.path.isdir(os.path.join(path, p))]
        return cls(name, path, *categories)
