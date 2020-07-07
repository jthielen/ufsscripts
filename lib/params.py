# Copyright (c) 2020 Jon Thielen.
# Distributed under the terms of the Apache 2.0 License.
# SPDX-License-Identifier: Apache-2.0
"""
Shared Arguments/Configuration Utils
--------------------------

"""

import argparse
from pathlib import Path

import yaml


# Open default configuration
with open(Path(__file__).parent / "../config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)


def create_parser(description):
    """Create a default ArgumentParser."""
    return argparse.ArgumentParser(
        description=description,
        usage=argparse.SUPPRESS
    )


def add_required_argument(parser, name, short_code, description, suggested=None):
    """Add a required argument to the given parser."""
    if name in config["defaults"] and suggested is None:
        suggested = config["defaults"][name]
    parser.add_argument(
        "-" + short_code,
        "--" + name,
        help="<Required> " + description,
        required=True,
        metavar=suggested
    )


def add_optional_argument(parser, name, short_code, description, default=None):
    """Add an optional argument to the given parser."""
    if name in config["defaults"] and default is None:
        default = config["defaults"][name]
    parser.add_argument(
        "-" + short_code,
        "--" + name,
        help=description,
        default=default,
        metavar=default
    )


def get_args(parser):
    """Get the cmd args from initialized parser, otherwise exiting with help."""
    try:
        args = vars(parser.parse_args())
        # Convert types (int)
        for var in config["typecast"]["int"]:
            if var in args:
                args[var] = int(args[var])
        for var in config["typecast"]["float"]:
            if var in args:
                args[var] = float(args[var])
        return args
    except SystemExit:
        parser.print_help()
        raise
