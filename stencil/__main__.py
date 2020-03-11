#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   stencil-blog, 2020
#   - blake
# <<

import os
import sys
import argparse
from argparse import Namespace
from typing import List

from stencil.config import load_config
from stencil.objects import Validation


def main(args: Namespace) -> int:
    """MAIN ENTRY POINT"""

    # load the config
    config = load_config(args.config)

    print(config)

    return 0


def validate_args(args: Namespace) -> Validation:
    """Takes a namespace of command line arguments and validates the values to ensure
    they won't choke up the rest of the program.

    Returns:
        (bool, List[str]):
    """

    err: List[str] = []

    if not os.path.isfile(args.config):
        err.append(f"{args.config} does not exist")
    else:
        args.config = os.path.abspath(args.config)

    return Validation(err)


# -- application entry point
if __name__ == "__main__":

    # fmt: off
    class Help:
        """Opinionated static site generator with extensive metadata support."""

        c = "Path to valid configuration file (TOML or JSON)"
        d = "Do not write anything to destination folder."

    p = argparse.ArgumentParser(
        prog="stencil",
        description=getattr(Help, '__doc__'),
        usage="%(prog)s [--config FILE] [options]")

    p.add_argument("--config",      "-c", default="stencil.toml", type=str, action="store", help=Help.c)
    p.add_argument("--dry-run",     "-d", default=False, action="store_true", help=Help.d)
    # fmt: on

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(0)

    args: Namespace = p.parse_args()
    valid: Validation = validate_args(args)

    if not valid.success:
        for err in valid.errors:
            sys.stderr.write(f"{err}\n")
        sys.stderr.flush()
        sys.exit(1)

    # done!!
    sys.exit(not bool(main(args)))
