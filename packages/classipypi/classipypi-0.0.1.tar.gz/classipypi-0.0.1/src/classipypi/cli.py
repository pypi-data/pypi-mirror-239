from sys import stderr
from textwrap import indent

import defopt
from pydantic import ValidationError

from .core import list_tags, select_tags
from .interfaces import ListingConfig, SelectorConfig

__all__ = ["run_cli"]

commands = {"sel": SelectorConfig, "ls": ListingConfig}


def handle_validation_error(ve: ValidationError) -> str:
    chosen_command = {v.__name__: k for k, v in commands.items()}[ve.title]
    error_msgs = "\n".join(str(e["ctx"]["error"]) for e in ve.errors())
    msg = f"Invalid {chosen_command!r} command:\n" + indent(error_msgs, prefix="- ")
    print(msg, end="\n\n", file=stderr)
    return chosen_command


def run_cli():
    try:
        config = defopt.run(commands, no_negated_flags=True)
    except ValidationError as ve:
        chosen_command = handle_validation_error(ve)
        try:
            defopt.run(commands[chosen_command], argv=["-h"], no_negated_flags=True)
        except SystemExit as exc:
            exc.code = 1
            raise
    else:
        match config:
            case SelectorConfig():
                print(f"Got {config=}")
                result = select_tags(config)
            case ListingConfig():
                result = list_tags(config)
        print("\n".join(result))
