============
pyexcel-text
============

.. image:: https://travis-ci.org/chfw/pyexcel-text.svg?branch=v0.0.1-rc1
    :target: https://travis-ci.org/chfw/pyexcel-text/builds/41650194

.. image:: https://coveralls.io/repos/chfw/pyexcel-text/badge.png?branch=v0.0.1-rc1 
    :target: https://coveralls.io/r/chfw/pyexcel-text?branch=v0.0.1-rc1 

.. image:: https://pypip.in/d/pyexcel-text/badge.png
    :target: https://pypi.python.org/pypi/pyexcel-text

.. image:: https://pypip.in/py_versions/pyexcel-text/badge.png
    :target: https://pypi.python.org/pypi/pyexcel-text

.. image:: https://pypip.in/implementation/pyexcel-text/badge.png
    :target: https://pypi.python.org/pypi/pyexcel-text


It is a plugin to `pyexcel <https://github.com/chfw/pyexcel>`__ and extends its capbility to present and write data in text fromats mainly through `tabulate`:

* "plain"
* "simple"
* "grid"
* "pipe"
* "orgtbl"
* "rst"
* "mediawiki"
* "latex"
* "latex_booktabs"
* "json"

Usage
======

    >>> import pyexcel as pe
    >>> import pyexcel.ext.text as text
    >>> content = [
    ...     ["Column 1", "Column 2", "Column 3"],
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [7, 8, 9]
    ... ]
    >>> sheet = pe.Sheet(content)
    >>> sheet
    Sheet Name: pyexcel
    --------  --------  --------
    Column 1  Column 2  Column 3
    1         2         3
    4         5         6
    7         8         9
    --------  --------  --------
    >>> sheet.name_columns_by_row(0)
    >>> sheet
    Sheet Name: pyexcel
      Column 1    Column 2    Column 3
    ----------  ----------  ----------
             1           2           3
             4           5           6
             7           8           9
    >>> multiple_sheets = {
    ...      'Sheet 1':
    ...          [
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0],
    ...              [7.0, 8.0, 9.0]
    ...          ],
    ...      'Sheet 2':
    ...          [
    ...              ['X', 'Y', 'Z'],
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0]
    ...          ],
    ...      'Sheet 3':
    ...          [
    ...              ['O', 'P', 'Q'],
    ...              [3.0, 2.0, 1.0],
    ...              [4.0, 3.0, 2.0]
    ...          ]
    ...  }
    >>> book = pe.Book(multiple_sheets)
    >>> text.TABLEFMT = "rst"
    >>> text.save_as(book, "myfile.rst")
    >>> myfile = open("myfile.rst")
    >>> print(myfile.read())
    Sheet Name: Sheet 1
    =  =  =
    1  2  3
    4  5  6
    7  8  9
    =  =  =
    Sheet Name: Sheet 2
    ===  ===  ===
    X    Y    Z
    1.0  2.0  3.0
    4.0  5.0  6.0
    ===  ===  ===
    Sheet Name: Sheet 3
    ===  ===  ===
    O    P    Q
    3.0  2.0  1.0
    4.0  3.0  2.0
    ===  ===  ===

.. testcode::
   :hide:

    >>> import os
    >>> os.unlink("myfile.rst")


Dependencies
============

* tabulate
