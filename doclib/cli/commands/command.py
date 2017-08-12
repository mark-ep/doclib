from abc import ABCMeta, abstractmethod
import argparse as ap
from typing import List


class Command(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """
        return unique command name
        """

    @classmethod
    @abstractmethod
    def parser_name(cls) -> str:
        """
        return unique command parser name
        """

    @classmethod
    @abstractmethod
    def help_line(cls) -> str:
        """
        return command description
        """

    @classmethod
    @abstractmethod
    def parser_kwargs(cls) -> dict:
        """
        return arguments for command parser
        """

    @classmethod
    def configure(cls, parser: ap.ArgumentParser) -> None:
        """
        configure the parser
        """

    @abstractmethod
    def execute(self, command_args: ap.Namespace):
        """
        execute this command
        """

class ChildCommand(Command, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def requires_parent_arguments(cls) -> bool:
        """
        indicates if this subcommand needs arguments from the parent
        """

class ParentCommand(Command, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def command_name(cls) -> str:
        """
        the name of the parser command
        """

    def execute(self, command_args: ap.Namespace):
        if hasattr(command_args, 'sub_command') and command_args.sub_command:
            return command_args.sub_command().execute(command_args)
        else:
            parser = getattr(command_args, self.parser_name())
            parser.print_help()

    @classmethod
    @abstractmethod
    def parent_arguments(cls) -> dict:
        """
        return dict of arguments to be considered by parent parser
        """

    @classmethod
    @abstractmethod
    def get_subparsers(cls) -> List[Command]:
        """
        return list of subparsers for this command
        """

    @classmethod
    def configure_parser_and_subparsers(cls, parser: ap.ArgumentParser, subparsers):
        parsers = {cls.parser_name(): parser}
        parser.set_defaults(**parsers)

        for subcommand in cls.get_subparsers():
            subparser = subparsers.add_parser(
                subcommand.name(), help=subcommand.help_line()
            )
            if subcommand.requires_parent_arguments():
                subparser.add_argument(**cls.parent_arguments())
            subcommand.configure(subparser)
            subparser.set_defaults(**{cls.command_name(): subcommand.execute})

    @classmethod
    def configure(cls, parser: ap.ArgumentParser):
        subparsers = parser.add_subparsers(
            dest='subcommand_name', metavar='COMMAND'
        )
        cls.configure_parser_and_subparsers(parser, subparsers)
