#!/bin/python

import re
import sys

from nvexpo import nvexpo
from nvexpo import consts as CONSTS


def main() -> int:
    args = sys.argv
    if len(args) <= 1:
        nvexpo.show_help()
        return 0

    if args[1] in ["--unset"]:
        nvexpo.unset_env(args[2:])
        return 0

    if args[1] in ["--load"]:
        nvexpo._load()
        return 0

    if args[1] in ["init"]:
        try:
            nvexpo.init(args[2])
        except IndexError:
            nvexpo.init()
        return 0

    raw_vars = args[1:]
    variables = {}
    for raw_var in raw_vars:
        if "=" not in raw_var:
            nvexpo.show_help('Use the syntax "key=value"')
            return 1
        try:
            key, value = raw_var.split("=", 1)
        except ValueError as e:
            nvexpo.show_help(f"Unexpected error {e}")
            return 1
        key = key.strip("=")
        value = value.strip("=").strip('"')
        variables[key] = value
        if not key:
            nvexpo.show_help("Empty name")
            return 1
        if not value:
            nvexpo.show_help("Empty value")
            return 1
        if not re.match(CONSTS.VARNAME_PATTERN, key):
            nvexpo.show_help(f'"{key}" is not a valid name')
            return 1
    nvexpo.set_env(variables)
    return 0


if __name__ == "__main__":
    sys.exit(main())
