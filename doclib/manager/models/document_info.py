from typing import List
import os
import stat
import time


class DocumentInfo:
    @property
    def name(self) -> str:
        """
        the name of the file
        """
        return self._name

    @property
    def path(self) -> str:
        """
        the path to the file
        """
        return self._path

    @property
    def edit_date(self) -> str:
        """
        date file was last edited
        """
        return self._edit_date

    @property
    def added_date(self) -> str:
        """
        date file was added to the library
        """
        return self._added_date

    @property
    def create_date(self) -> str:
        """
        date file was originally created
        """
        return self._create_date

    @property
    def size(self) -> str:
        """
        size (in bytes) of the file
        """
        return self._size

    @property
    def tags(self) -> List[str]:
        """
        tags associated with the file
        """
        return self._tags

    @property
    def is_default(self) -> bool:
        return self._default

    def __init__(self, name: str, path: str=None, size: int=None,
                 edate: str=None, adate: str=None, cdate: str=None,
                 *tags: str):
        self._name = name
        self._path = path
        self._size = size
        self._edit_date = edate
        self._added_date = adate
        self._create_date = cdate
        self._tags = tags

    @classmethod
    def from_path(cls, path) -> "DocumentInfo":
        basename = os.path.basename(path)
        name, _ = os.path.splitext(basename)

        info = os.stat(path)
        size = info[stat.ST_SIZE]
        edate = time.asctime(time.localtime(info[stat.ST_MTIME]))

        return cls(name=name, path=path, size=size, edate=edate)
