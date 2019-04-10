.. |ReST| replace:: *reStructuredText*
.. |copy| unicode:: 0xA9 .. знак копирайта
.. |date| date:: %d.%m.%Y
.. |time| date:: %H:%M


Welcome to ConfigRW documentation!
=====================================

ConfigRW is a simple python module which read and write config files
based on key-value or INI-structure.

Key features
------------

* Maximum preserves formatting of the source file (indents, spaces, comments, etc)
* Support non-section (for access for simple config files based on key-value)
* Inserting an option on an arbitrary string in the section
* Support multiple values of option
* Support options without values
* Support comments in a section
* Support indentation for options, values
* Secure file rewriting. Using `*.new` file on write, then renamed to original filename

Table of contents
-----------------

.. toctree::
    :numbered:
    :maxdepth: 1

    installation
    quickstart
    loadconfig
    sections
    items
    print
    write
