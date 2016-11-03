Advanced formatting
===================


* ``{num}`` int_
* ``{name}`` str_
* ``{symbol}`` str_
* ``{variant}`` str_
* ``{current_data}`` group_data_
* ``{count}`` int_
* ``{names}`` list_of_str_
* ``{symbols}`` list_of_str_
* ``{variants}`` list_of_str_
* ``{all_data}`` list_of_group_data_


``int``
+++++++

See `Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>`__


``str``
+++++++

See `Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>`__


.. _list_of_str:

``list`` of ``str``
+++++++++++++++++++

    | ``format_spec ::= [str_format_spec][:[join_str]]``

    | ``str_format_spec`` — str_
    | ``join_str`` — ``str`` used to join list elements


.. _group_data:

``GroupData``
+++++++++++++

    | ``format_spec ::= [format_str]``

    | ``format_str`` — arbitrary format string, where the only replacent
      strings are ``{num}``, ``{name}``, ``{symbol}`` and ``{variant}``.


.. _list_of_group_data:

``list`` of ``GroupData``
+++++++++++++++++++++++++

    | ``format_spec ::= [group_data_format_spec][:[join_str]]``

    | ``group_data_format_spec`` — group_data_
    | ``join_str`` — ``str`` used to join list elements
