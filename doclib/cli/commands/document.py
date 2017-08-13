from .command import ParentCommand, Command
import argparse as ap
from typing import List

from doclib.manager import Manager


class AddDocument(Command):
    CMD_NAME = 'add'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='document_name', metavar='DOCUMENT',
                            help='name of the document')
        parser.add_argument(dest='document_path', metavar='PATH',
                            help='location of the document')
        parser.add_argument('-rev', '--revision', metavar='REVISION',
                            help='revision number of document')
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument('--copy', action='store_true',
                          help='leave original file in place')
        mode.add_argument('--link', action='store_true',
                          help='create link to original file')
        parser.add_argument('-nl', '--notlatest', action='store_true',
                            help='do not replace current latest revision')
        parser.add_argument('-tags', metavar='TAG', nargs='+',
                            help='meta-tags for the file')

    @classmethod
    def parser_kwargs(cls):
        help_line = "Add a document."
        return dict(help=help_line, description=help_line)

    def execute(self, arguments: ap.Namespace):
        pass


class ListDocuments(Command):
    CMD_NAME = 'list'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "List documents."
        return dict(aliases=['ls'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')

    def execute(self, arguments: ap.Namespace):
        documents = Manager.get_documents(arguments.project_name)
        if not documents:
            print("no documents\n")
        else:
            print("%i documents:" % len(documents))
            for doc in documents:
                print("  %s" % doc['name'])
            print()

class RemoveDocument(Command):
    CMD_NAME = 'remove'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Remove a document."
        return dict(aliases=['rm'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='document_name', metavar='DOCUMENT',
                            help='name of the document')
        parser.add_argument('-rev', '--revision', metavar='REVISION',
                            help='revision number of document')
        parser.add_argument('-f', '--force', action='store_true',
                            help="do not check if project has contents.")

    def execute(self, arguments: ap.Namespace):
        pass


class CopyDocument(Command):
    CMD_NAME = 'copy'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Copy a document."
        return dict(aliases=['cp'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        pass

    def execute(self, arguments: ap.Namespace):
        pass

class MoveDocument(Command):
    CMD_NAME = 'move'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Move a document."
        return dict(aliases=['mv'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        pass

    def execute(self, arguments: ap.Namespace):
        pass


class InspectDocument(Command):
    CMD_NAME = 'info'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Inspect a document."
        return dict(aliases=['i'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='document_name', metavar='DOCUMENT',
                            help='name of the document')

    def execute(self, arguments: ap.Namespace):
        info = Manager.get_document(
            arguments.project_name, arguments.document_name
        )
        print(info['name'])
        print(info['description'])


class Document(ParentCommand):
    CMD_NAME = 'document'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Manage documents."
        return dict(aliases=['doc'], help=help_line, description=help_line)

    @classmethod
    def subcommands(cls) -> List[Command]:
        return [
            AddDocument,
            ListDocuments,
            RemoveDocument,
            CopyDocument,
            MoveDocument,
            InspectDocument
            # OpenDocument,
            # SetCurrentRevision,
            # TagDocument
        ]
