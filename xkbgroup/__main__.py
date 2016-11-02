# -*- coding: utf-8 -*-

import os
import sys

from argparse import ArgumentParser

from .core import XKeyboard
from .version import print_version


GET_CHOICES = ["num", "name", "symbol", "variant",
               "count", "names", "symbols", "variants"]
SET_CHOICES = ["num", "name", "symbol"]


def xkb_get(args, xkb):
    attrmap = {
        "num": "group_num",
        "name": "group_name",
        "symbol": "group_symbol",
        "variant": "group_variant",
        "count": "groups_count",
        "names": "groups_names",
        "symbols": "groups_symbols",
        "variants": "groups_variants",
    }

    value = getattr(xkb, attrmap[args.attribute])
    value = "\n".join(value) if isinstance(value, list) else value

    print(value)

def xkb_set(args, xkb):
    value = int(args.value) if args.attribute == "num" else args.value
    attrmap = {
        "num": "group_num",
        "name": "group_name",
        "symbol": "group_symbol",
    }

    setattr(xkb, attrmap[args.attribute], value)


def create_argument_parser():
    parser = ArgumentParser()

    parser.add_argument("-V", "--version", action="store_true")
    subparsers = parser.add_subparsers(title="actions", dest="cmd")
    #subparsers.required = True

    parser_get = subparsers.add_parser("get")
    parser_get.set_defaults(func=xkb_get)
    parser_get.add_argument("attribute", choices=GET_CHOICES)

    parser_set = subparsers.add_parser("set")
    parser_set.set_defaults(func=xkb_set)
    parser_set.add_argument("attribute", choices=SET_CHOICES)
    parser_set.add_argument("value")

    return parser

def main():
    xkb = XKeyboard()
    progname = os.path.basename(sys.argv[0])

    parser = create_argument_parser()
    args = parser.parse_args()
    if args.version:
        print_version(progname)
    elif args.cmd:
        args.func(args, xkb)
    else:
        parser.print_usage(sys.stderr)
        parser.exit(2, "{prog}: error: {message}\n".format(
            prog=progname,
            message="the following arguments are required: cmd"))

if __name__ == '__main__':
    main()
