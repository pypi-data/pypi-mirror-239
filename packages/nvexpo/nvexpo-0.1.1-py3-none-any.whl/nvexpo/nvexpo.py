from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path
from typing import IO, Any

ENV_VARS = Path.home() / ".nvexpo.env"


class Mode(Enum):
    R = "r"
    W = "w"


class Cmd(Enum):
    Set = "export"
    Unset = "unset"


def _get_file(mode: Mode) -> IO[Any]:
    return ENV_VARS.open(mode.value)


def _get_saved_vars() -> dict[str, str]:
    output = {}
    with _get_file(Mode.R) as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            key, value = line.split("=", 1)
            output[key] = value
    return output


def _save_vars(variables: dict[str, str]) -> None:
    new_variables = []
    for key, value in variables.items():
        if "'" in value:
            comma = '"'
        elif '"' in value:
            comma = "'"
        else:
            comma = ""

        new_variables.append(f"{key}={comma}{value}{comma}")

    with _get_file(Mode.W) as file:
        file.write("\n".join(new_variables))


def _print_bulk(attrs: list[str], cmd: Cmd) -> None:
    for attr in attrs:
        print(f"{cmd.value} {attr}")


def _load() -> None:
    current_vars = _get_saved_vars()
    attrs = [f"{key}={value}" for key, value in current_vars.items()]
    _print_bulk(attrs, Cmd.Set)


def set_env(variables: dict[str, str]) -> None:
    current_vars = _get_saved_vars()
    current_vars.update(variables)
    _save_vars(current_vars)
    _load()


def unset_env(variables: list[str]) -> None:
    current_vars = _get_saved_vars()
    for var in variables:
        current_vars.pop(var, None)
    _save_vars(current_vars)
    _print_bulk(variables, Cmd.Unset)


def show_help(error: None | str = None) -> None:
    msg = """
    nx: Non-Volatile Export

    Basic usage:
    - Set a simple var
    $ nx VAR1="hello world"
    $ echo VAR1
    hello world

    - Unset the variable
    $ nx --unset VAR1
    $ echo VAR1
    <nothing>

    - Persist into bash sessions
    $ bash
    $ nx VAR1="hello world"
    $ exit
    $ bash
    $ echo $VAR1
    hello world
    """.strip()
    msg = "\n".join(map(str.strip, msg.splitlines()))
    if error is not None:
        msg = f"Error: {error}\n\n" + msg
    print(msg, file=sys.stderr)


def init(shell: str | None = None) -> None:
    if shell is None:
        shell = "bash"

    if shell == "bash":
        cmd = """
        function nx(){
            eval "$(nvexpo $@)"
        }
        """
        print(cmd)
        _load()


if not ENV_VARS.exists():
    _get_file(Mode.W).close()
