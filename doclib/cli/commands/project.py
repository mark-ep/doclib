from .command import ParentCommand, Command
import argparse as ap
from typing import List

from doclib.manager import Manager


class AddProject(Command):
    CMD_NAME = 'add'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument('-d', '--desc', dest='description',
                            metavar='DESCRIPTION',
                            help='description of the project')

    @classmethod
    def parser_kwargs(cls):
        help_line = "Add a project."
        return dict(help=help_line, description=help_line)

    def execute(self, arguments: ap.Namespace):
        project = Manager.add_project(
            arguments.project_name, arguments.description
        )
        print("created new project: %s\n" % arguments.project_name)


class ListProjects(Command):
    CMD_NAME = 'list'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "List projects."
        return dict(aliases=['ls'], help=help_line, description=help_line)

    def execute(self, arguments: ap.Namespace):
        projects = Manager.get_projects()
        if not projects:
            print("no projects\n")
        else:
            print("%i projects:" % len(projects))
            for project in projects:
                print("  %s" % project['name'])
            print()

class RemoveProject(Command):
    CMD_NAME = 'remove'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Remove a project."
        return dict(aliases=['rm'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument('-f', '--force', action='store_true',
                            help="do not check if project has contents.")

    def execute(self, arguments: ap.Namespace):
        Manager.remove_project(arguments.project_name, recursive=arguments.force)
        print("deleted project: %s" % arguments.project_name)


class CopyProject(Command):
    CMD_NAME = 'copy'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Copy a project."
        return dict(aliases=['cp'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='new_name', metavar='NEWNAME',
                            help='name of copy')

    def execute(self, arguments: ap.Namespace):
        Manager.copy_project(arguments.project_name, arguments.new_name)

class MoveProject(Command):
    CMD_NAME = 'move'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Move a project."
        return dict(aliases=['mv'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')
        parser.add_argument(dest='new_name', metavar='NEWNAME',
                            help='new name of project')

    def execute(self, arguments: ap.Namespace):
        Manager.move_project(arguments.project_name, arguments.new_name)


class InspectProject(Command):
    CMD_NAME = 'info'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Inspect a project."
        return dict(aliases=['i'], help=help_line, description=help_line)

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        parser.add_argument(dest='project_name', metavar='PROJECT',
                            help='name of the project')

    def execute(self, arguments: ap.Namespace):
        info = Manager.get_project(arguments.project_name)
        print(info['name'])
        print(info['description'])


class Project(ParentCommand):
    CMD_NAME = 'project'

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_kwargs(cls):
        help_line = "Manage projects."
        return dict(aliases=['p'], help=help_line, description=help_line)

    @classmethod
    def subcommands(cls) -> List[Command]:
        return [
            AddProject,
            ListProjects,
            RemoveProject,
            CopyProject,
            MoveProject,
            InspectProject
        ]
