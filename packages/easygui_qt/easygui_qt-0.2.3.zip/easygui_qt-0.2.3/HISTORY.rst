.. :changelog:

History
=======

0.2.3
-----

- added demos dir to setup.py so that it can be included on pypi

0.2.2a
------

- changing path on image in readme in attempt to help pypi display properly

0.2.2
-----

- changed the syntax for calls to super() to be compatible with Python 2.
  Note that the intention is to be a Python 3 project, but if simple changes
  can make it compatible with Python 2, they will be incorporated.
- changed name of set_save_file_name to get_save_file_name
- changed name of yes_no_question to get_yes_or_no
- added get_list_of_choices
- added demo launcher

0.2.1
-----

- Moved the demos directory to a more sensible location
- added get_directory_name
- added get_file_names
- added set_save_file_name
- attempt to fix bug for Python 3.2 where inspect.signature was not defined

0.2.0
------

The API has been changed since the initial release
and the following widgets have been documented, with images inserted
in the documentation.

- get_choice
- get_float
- get_int
- get_integer
- get_string
- set_font_size
- set_default_font
- select_language
- set_locale
- show_message
- yes_no_question

0.1.0
---------------------

* First release on PyPI.
