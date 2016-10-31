import re
import sys

from ctypes import *
from collections import namedtuple

from .xkb import *


# Error-related utilities

OPEN_DISPLAY_ERRORS = {
    XkbOD_BadLibraryVersion: "Compile-time and runtime XKB libraries not compatible",
    XkbOD_ConnectionRefused: "Display could not be opened",
    XkbOD_BadServerVersion: "Library and server have incompatible XKB versions",
    XkbOD_NonXkbServer: "XKB not present in the X server"
}

GET_CONTROLS_ERRORS = {
    BadAlloc: "Unable to allocate storage",
    BadImplementation: "Invalid reply from server",
    BadMatch: "A compatible version of Xkb was not available in the server or "
              "an argument has correct type and range, but is otherwise invalid"
}

GET_NAMES_ERRORS = {
    BadAlloc: "Unable to allocate storage",
    BadImplementation: "Invalid reply from server",
    BadLength: "The length of a request is shorter or longer than that "
               "required to minimally contain the arguments",
    BadMatch: "A compatible version of Xkb was not available in the server or "
              "an argument has correct type and range, but is otherwise invalid"
}

class X11Error(Exception):
    pass

def _ensure_type(obj, type):
    if not isinstance(obj, type):
        raise ValueError("Wrong value type, must be {}.".format(str(type)))


class XKeyboard:
    # Main methods

    def __init__(self, auto_open=True):
        if auto_open:
            self.open_display()

    def open_display(self):
        self.close_display()    # Properly finish previous open_display()

        XkbIgnoreExtension(False)

        display_name = None
        major = c_int(XkbMajorVersion)
        minor = c_int(XkbMinorVersion)
        reason = c_int()

        self._display = XkbOpenDisplay(
            display_name,
            None, None, byref(major), byref(minor), byref(reason))
        if reason.value in OPEN_DISPLAY_ERRORS:
            raise X11Error(OPEN_DISPLAY_ERRORS[reason.value] + ".")

        self._keyboard_description = XkbGetMap(self._display, 0, XkbUseCoreKbd)
        if not self._keyboard_description:
            self.close_display()
            raise X11Error("Failed to get keyboard description.")

        # Controls mask doesn't affect the availability of xkb->ctrls->num_groups anyway
        # Just use a valid value, and xkb->ctrls->num_groups will be definitely set
        status = XkbGetControls(self._display, XkbAllControlsMask, self._keyboard_description)
        if status != Success:
            self.close_display()
            raise X11Error(GET_CONTROLS_ERRORS[status] + ".")

        names_mask = XkbSymbolsNameMask | XkbGroupNamesMask
        status = XkbGetNames(self._display, names_mask, self._keyboard_description)
        if status != Success:
            self.close_display()
            raise X11Error(GET_NAMES_ERRORS[status] + ".")

    def close_display(self):
        if hasattr(self, "_keyboard_description") and self._keyboard_description:
            names_mask = XkbSymbolsNameMask | XkbGroupNamesMask
            XkbFreeNames(self._keyboard_description, names_mask, True)
            XkbFreeControls(self._keyboard_description, XkbAllControlsMask, True)
            XkbFreeClientMap(self._keyboard_description, 0, True)
            del self._keyboard_description

        if hasattr(self, "display") and self._display:
            XCloseDisplay(self._display)
            del self._display

    def __del__(self):
        self.close_display()

    def __enter__(self):
        self.open_display()
        return self

    def __exit__(self, type, value, traceback):
        self.close_display()


    # Properties for all layouts

    @property
    def groups_count(self):
        if self._keyboard_description.contents.ctrls is not None:
            return self._keyboard_description.contents.ctrls.contents.num_groups
        else:
            groups_source = self._groups_source

            groups_count = 0
            while (groups_count < XkbNumKbdGroups and
                   groups_source[groups_count] != None_):
                groups_count += 1

            return groups_count

    @property
    def groups_names(self):
        return [self._get_group_name_by_num(i) for i in range(self.groups_count)]

    @property
    def groups_symbols(self):
        return [symdata.symbol for symdata in self._symboldata_list]

    @property
    def groups_variants(self):
        return [symdata.variant or "" for symdata in self._symboldata_list]


    # Properties and methods for current layout

    @property
    def group_num(self):
        xkb_state = XkbStateRec()
        XkbGetState(self._display, XkbUseCoreKbd, byref(xkb_state))
        return xkb_state.group

    @group_num.setter
    def group_num(self, value):
        _ensure_type(value, int)
        if XkbLockGroup(self._display, XkbUseCoreKbd, value):
            XFlush(self._display)
        else:
            self.close_display()
            raise X11Error("Failed to set group number.")


    @property
    def group_name(self):
        return self._get_group_name_by_num(self.group_num)

    @group_name.setter
    def group_name(self, value):
        _ensure_type(value, str)
        groups_names = self.groups_names
        n_mapping = {groups_names[i]: i for i in range(len(groups_names))}
        try:
            self.group_num = n_mapping[value]
        except KeyError as exc:
            raise ValueError("Wrong group name.") from exc


    @property
    def group_symbol(self):
        s_mapping = {symdata.index: symdata.symbol for symdata in self._symboldata_list}
        return s_mapping[self.group_num]

    @group_symbol.setter
    def group_symbol(self, value):
        _ensure_type(value, str)
        s_mapping = {symdata.symbol: symdata.index for symdata in self._symboldata_list}
        try:
            self.group_num = s_mapping[value]
        except KeyError as exc:
            raise ValueError("Wrong group symbol.") from exc


    @property
    def group_variant(self):
        v_mapping = {symdata.index: symdata.variant for symdata in self._symboldata_list}
        return v_mapping[self.group_num] or ""

    # Current group variant is a get-only value because variants are associated
    # with symbols in /usr/share/X11/xkb/rules/evdev.lst and specified at
    # setxkbmap call time


    # Private properties and methods

    @property
    def _groups_source(self):
        return self._keyboard_description.contents.names.contents.groups

    @property
    def _symbols_source(self):
        return self._keyboard_description.contents.names.contents.symbols

    @property
    def _symboldata_list(self):
        symbol_str_atom = self._symbols_source
        if symbol_str_atom != None_:
            b_symbol_str = XGetAtomName(self._display, symbol_str_atom)
            return _parse_symbols(b_symbol_str.decode(), ["pc", "inet", "group"])
        else:
            raise X11Error("Failed to get symbol names.")

    def _get_group_name_by_num(self, group_num):
        cur_group_atom = self._groups_source[group_num]
        if cur_group_atom != None_:
            b_group_name = XGetAtomName(self._display, cur_group_atom)
            return b_group_name.decode() if b_group_name else ""
        else:
            raise X11Error("Failed to get group name.")


SymbolData = namedtuple("SymbolData", ["symbol", "variant", "index"])
SYMBOL_REGEX = re.compile(r"""
    (?P<symbol>\w+)
    (?: \( (?P<variant>\w+) \) )?
    (?: : (?P<index>\d+) )?
    """, re.VERBOSE)

class _Compat_SRE_Pattern:
    def __init__(self, re_obj):
        self.re_obj = re_obj

    def __getattr__(self, name):
        return getattr(self.re_obj, name)

    # re_obj.fullmatch is a Python 3.4+ only feature
    def fullmatch(self, string, pos=None, endpos=None):
        pos = pos if pos else 0
        endpos = endpos if endpos else len(string)
        match = self.re_obj.match(string, pos, endpos)
        if match and match.span() != (pos, endpos):
            return None
        return match

if sys.version_info < (3, 4):
    SYMBOL_REGEX = _Compat_SRE_Pattern(SYMBOL_REGEX)

def _parse_symbols(symbols_str, non_symbols, default_index=0):
    def get_symboldata(symstr):
        match = SYMBOL_REGEX.fullmatch(symstr)
        if match:
            index = match.group('index')
            return SymbolData(
                match.group('symbol'),
                match.group('variant'),
                int(index) - 1 if index else default_index)
        else:
            raise X11Error("Malformed symbol string: \"{}\"".format(symstr))

    symboldata_list = []
    for symstr in symbols_str.split('+'):
        symboldata = get_symboldata(symstr)
        if symboldata.symbol not in non_symbols:
            symboldata_list.append(symboldata)

    indices = [symdata.index for symdata in symboldata_list]
    assert len(indices) == len(set(indices))    # No doubles

    return symboldata_list


__all__ = ["XKeyboard", "X11Error"]


def print_xkeyboard(xkb):
    print("xkb {")
    contents = [
        "%d groups {%s}," % (xkb.groups_count, ", ".join(xkb.groups_names)),
        "symbols {%s}" % ", ".join(xkb.groups_symbols),
        "variants {%s}" % ", ".join('"{}"'.format(variant) for variant in xkb.groups_variants),
        "current group: %s (%d) - %s - \"%s\"" %
            (xkb.group_symbol, xkb.group_num, xkb.group_name, xkb.group_variant)
    ]
    print("\n".join("\t" + line for line in contents))
    print("}")

def test():
    with XKeyboard() as xkb:
        print_xkeyboard(xkb)
        xkb.group_num += 2
        print_xkeyboard(xkb)
        xkb.group_num -= 3
        print_xkeyboard(xkb)
        xkb.group_num -= 2
        print_xkeyboard(xkb)

if __name__ == '__main__':
    test()
