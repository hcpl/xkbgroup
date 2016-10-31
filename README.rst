========
xkbgroup
========

.. image:: https://img.shields.io/badge/python-3.2+-blue.svg

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/hcpl/xkbgroup/blob/master/LICENSE

Use this library to change the keyboard layout through XKB extension (subsystem)
of the X server system.


Dependencies
------------

* Python 3.2+
* ``libX11.so.6`` shared library which you must have by default if you use
  X server


Usage
-----

.. code-block:: sh

   # Assume we have the following configuration
   $ setxkbmap -layout us,ru,ua,fr
   $ python

.. code-block:: python

   >>> from xkbgroup import XKeyboard
   >>> xkb = XKeyboard()
   >>> xkb.group_num
   1
   >>> xkb.group_num = 2
   >>> xkb.group_num
   2
   >>> xkb.group_num -= 2
   >>> xkb.group_num
   0
   >>> xkb.group_name
   English (US)
   >>> xkb.group_name = 'Ukrainian'
   >>> xkb.group_name
   Ukrainian
   >>> xkb.group_num
   2
   >>> xkb.group_symbol
   ua
   >>> xkb.group_symbol = 'fr'
   >>> xkb.group_symbol
   fr
   >>> xkb.group_variant
   ''
   >>> xkb.group_num -= 3
   >>> xkb.group_variant
   ''
   >>> xkb.group_num
   0
   >>>


Naming convention
-----------------

Throughout the whole XKB subsystem the `so-called groups represent actual
keyboard layouts`__. This library follows the same convention and names of the
API methods start with ``group_`` or ``groups_``.

__ https://wiki.archlinux.org/index.php/X_KeyBoard_extension#Keycode_translation


Classes
-------

These all reside in ``xkbgroup/core.py``:

* ``XKeyboard`` — the main class:

  - ``__init__(self, auto_open=True)`` — if ``auto_open`` is ``True``
    automatically call ``open_display()``.
  - ``open_display()`` — establishes connection with X server and prepares
    objects necessary to retrieve and send data.
  - ``close_display()`` — closes connection with X server and cleans up
    objects created on ``open_display()``.
  - ``group_*`` — properties for accessing current group data:

    + ``group_num`` — get/set current group number
      (e.g. ``0``, ``2``, ``3``).
    + ``group_name`` — get/set current group full name
      (e.g. ``English (US)``, ``Russian``, ``French``).
    + ``group_symbol`` — get/set current group symbol
      (e.g. ``us``, ``ru``, ``fr``).
    + ``group_variant`` — get (only) current group variant
      (e.g. `` ``, ``dos``, ``latin9``)
  - ``groups_*`` — properties for querying info about all groups set by
    ``setxkbmap``

    + ``groups_count`` — get number of all groups.
    + ``groups_names`` — get names of all groups.
    + ``groups_symbols`` — get symbols of all groups.
    + ``groups_variants`` — get variants of all groups.

* ``X11Error`` — an exception class, raised for errors on X server issues.


Helper files
------------

There are also complementary files:

* ``generate_bindings.sh`` — a shell script which generates Python bindings
  to X server structures, functions and ``#define`` definitions by:

  - converting X11 C headers using ``h2xml`` and ``xml2py``;
  - creating ``ctypes`` references to functions from ``libX11.so.6`` using
    ``xml2py``.

* ``xkbgroup/xkb.py`` — the output of the above script, usable for Xlib
  development under Python.
