from argparse import ArgumentParser

from .core import XKeyboard


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
    subparsers = parser.add_subparsers(title="actions")

    parser_get = subparsers.add_parser("get")
    parser_get.set_defaults(func=xkb_get)
    parser_get.add_argument("attribute", choices=GET_CHOICES)
    get_all_or_current = parser_get.add_mutually_exclusive_group()
    get_all_or_current.add_argument("-a", "--all", dest="get_all", action="store_true")
    get_all_or_current.add_argument("-c", "--current", dest="get_all", action="store_false")

    parser_set = subparsers.add_parser("set")
    parser_set.set_defaults(func=xkb_set)
    parser_set.add_argument("attribute", choices=SET_CHOICES)
    parser_set.add_argument("value")
    set_all_or_current = parser_set.add_mutually_exclusive_group()
    set_all_or_current.add_argument("-a", "--all", dest="get_all", action="store_true")
    set_all_or_current.add_argument("-c", "--current", dest="get_all", action="store_false")

    return parser

def main():
    xkb = XKeyboard()

    parser = create_argument_parser()
    args = parser.parse_args()
    args.func(args, xkb)

if __name__ == '__main__':
    main()
