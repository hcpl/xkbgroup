========
xkbgroup
========

Use this library to change the keyboard layout through XKB extension (subsystem)
of the X server system.


Naming convention
-----------------

Throughout the whole XKB subsystem the `so-called groups represent actual
keyboard layouts`__. This library follows the same convention and names of the
API methods start with ``group_`` or ``groups_``.

__ https://wiki.archlinux.org/index.php/X_KeyBoard_extension#Keycode_translation


Classes
-------

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
      (e.g. `` ``, ``dos``, ``latin9``)
  - ``groups_*`` — properties for querying info about all groups set by
    ``setxkbmap``

    + ``groups_count`` — get number of all groups.
    + ``groups_names`` — get names of all groups.
    + ``groups_symbols`` — get symbols of all groups.
    + ``groups_variants`` — get variants of all groups.

* ``X11Error`` — an exception class, raised for errors on X server issues.
