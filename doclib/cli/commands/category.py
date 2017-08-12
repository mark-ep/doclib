from .command import ParentCommand, Command
import argparse as ap
from typing import List

from doclib.manager import Manager


class AddCategory(Command):
    CMD_NAME = 'add'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='category_name', metavar='CATEGORY',
                            help='name of the category')

    @classmethod
    def parser_kwargs(cls):
        help_line = "Add a category."
        return dict(help=help_line, description=help_line)

    def execute(self, arguments: ap.Namespace):
        category =\
            Manager.add_category(arguments.project_name, arguments.category_name)
        print("created new category: %s\n" % category.path)


class ListCategories(Command):
    CMD_NAME = 'list'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')

    @classmethod
    def parser_kwargs(cls):
        help_line = "List categories."
        return dict(aliases=['ls'], help=help_line, description=help_line)

    def execute(self, arguments: ap.Namespace):
        categories = Manager.get_categories(arguments.project_name)
        if not categories:
            print("no categories\n")
        else:
            print("%i categories:" % len(categories))
            for category in categories:
                print("  %s" % category.name)
            print()

class RemoveCategory(Command):
    CMD_NAME = 'remove'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Remove a category."
        return dict(aliases=['rm'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='category_name', metavar='CATEGORY',
                            help='name of the category')
        parser.add_argument('-f', '--force', action='store_true',
                            help="do not check if category has contents.")

    def execute(self, arguments: ap.Namespace):
        Manager.remove_category(arguments.project_name, arguments.category_name,
                               recursive=arguments.force)
        print("deleted category: %s" % arguments.category_name)


class Category(ParentCommand):
    CMD_NAME = 'category'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Manage categories."
        return dict(aliases=['c'], help=help_line, description=help_line)

    @classmethod
    def subcommands(cls) -> List[Command]:
        return [
            AddCategory,
            ListCategories,
            RemoveCategory
        ]
