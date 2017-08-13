from .command import Command
import argparse as ap
from typing import List

from doclib.manager import Manager


class Tags(Command):
    CMD_NAME = 'tags'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "List tags."
        return dict(help=help_line, description=help_line)

    def execute(self, arguments: ap.Namespace):
        tags = Manager.list_tags()
        if not tags:
            print("no tags\n")
        else:
            print("%i tags:" % len(tags))
            for tag in tags:
                print("  %s" % tag['tag'])


class Search(Command):
    CMD_NAME = 'search'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Search tags."
        return dict(aliases=['s'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='tags', metavar='TAG', nargs='+',
                            help='tags to search for')

    def execute(self, arguments: ap.Namespace):
        documents = Manager.search_tags(*arguments.tags)
        if not documents:
            print("no results\n")
        else:
            print("%i results:" % len(documents))
            for doc in documents:
                print("  %s" % doc['name'])
            print()
