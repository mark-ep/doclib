from .command import ParentCommand, ChildCommand
import argparse as ap
from typing import List

from doclib.manager import Manager


class AddProject(ChildCommand):
    @classmethod
    def requires_parent_arguments(cls) -> bool:
        return True

    def excute(cls, arguments: ap.Namespace):
        Manager.add_project(arguments.project_name)
        print("created new project: %s\n" % arguments.project_name)


class ListProjects(ChildCommand):
    @classmethod
    def requires_parent_arguments(cls) -> bool:
        return False

    def excute(cls, arguments: ap.Namespace):
        projects = Manager.get_projects()
        if not projects:
            print("no projects\n")
        else:
            print("%i projects:" % len(projects))
            for project in projects:
                print("  %s" % project.name)
            print()


class Project(ParentCommand):
    CMD_NAME = 'project'
    HELP_LINE = 'Manage projects'

    @classmethod
    def help_line(cls) -> str:
        return cls.HELP_LINE

    @classmethod
    def name(cls) -> str:
        return cls.CMD_NAME

    @classmethod
    def parser_name(cls) -> str:
        return "project"

    @classmethod
    def command_name(cls) -> str:
        return "proj_command"

    @classmethod
    def parser_kwargs(cls):
        help_line = cls.help_line()
        return dict(aliases=['p', 'proj'], help=help_line, description=help_line)

    @classmethod
    def get_subparsers(cls) -> List[ChildCommand]:
        return [
            AddProject,
            ListProjects
        ]

    @classmethod
    def parent_arguments(cls) -> dict:
        return dict(
            dest='project_name', metavar='PROJECT', help='name of the project'
        )
