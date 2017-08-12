import pkg_resources
import argparse as ap


def load_commands() -> list:
    commands = []
    for entry_point in pkg_resources.iter_entry_points('doclib_commands'):
        commands.append(entry_point.load())

    return commands

def create_parser(name: str, desc: str, version: str) -> ap.ArgumentParser:
    commands = load_commands()

    parser = ap.ArgumentParser(
        prog=name, description='%s, version %s' % (desc, version)
    )
    parser.add_argument('--version', action='version', version='%s, %s' % (name, version))
    subparsers = parser.add_subparsers(
        dest='command_name', metavar='COMMAND'
    )
    for command_cls in commands:
        command_name = command_cls.name()
        command_args = command_cls.parser_kwargs()
        command_parser = subparsers.add_parser(command_name, **command_args)
        command_cls.configure(command_parser)
        command_parser.set_defaults(command_class=command_cls)

    return parser
