Advanced formatting
===================


==================  ======================
Replacement string           Type
==================  ======================
``{num}``           |int|_
``{name}``          |str|_
``{symbol}``        |str|_
``{variant}``       |str|_
``{current_data}``  |group_data|_
``{count}``         |int|_
``{names}``         |list_of_str|_
``{symbols}``       |list_of_str|_
``{variants}``      |list_of_str|_
``{all_data}``      |list_of_group_data|_
==================  ======================

.. |int| replace:: ``int``
.. |str| replace:: ``str``
.. |group_data| replace:: ``GroupData``
.. |list_of_str| replace:: ``list`` of ``str``
.. |list_of_group_data| replace:: ``list`` of ``GroupData``


|int|
+++++

See `Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>`__


|str|
+++++

See `Format Specification Mini-Language <https://docs.python.org/3/library/string.html#formatspec>`__


|list_of_str|
+++++++++++++

| ``format_spec ::= [str_format_spec][:[join_str]]``

| ``str_format_spec`` — str_
| ``join_str`` — ``str`` used to join list elements


|group_data|
+++++++++++++

| ``format_spec ::= [format_str]``

| ``format_str`` — arbitrary format string, where the only replacement
  strings are ``{num}``, ``{name}``, ``{symbol}`` and ``{variant}``.


|list_of_group_data|
++++++++++++++++++++

| ``format_spec ::= [group_data_format_spec][:[join_str]]``

| ``group_data_format_spec`` — |group_data|_
| ``join_str`` — ``str`` used to join list elements
