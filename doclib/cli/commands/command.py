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

class ParentCommand(Command, metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def subcommands(cls) -> List[Command]:
        """
        the subcommands of this command
        """

    @classmethod
    def configure(cls, parser: ap.ArgumentParser) -> None:
        subparsers = parser.add_subparsers(
            dest='subcommand_name', metavar='COMMAND'
        )
        for command_cls in cls.subcommands():
            command_name = command_cls.name()
            command_args = command_cls.parser_kwargs()
            command_parser = subparsers.add_parser(command_name, **command_args)
            command_cls.configure(command_parser)
            command_parser.set_defaults(subcommand_class=command_cls)

    def execute(self, command_args: ap.Namespace):
        if command_args.subcommand_name and command_args.subcommand_class:
            name = command_args.subcommand_name
            command = command_args.subcommand_class()

            command.execute(command_args)
