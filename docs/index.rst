

.. |ReST| replace:: *reStructuredText*
.. |copy| unicode:: 0xA9 .. знак копирайта
.. |date| date:: %d.%m.%Y
.. |time| date:: %H:%M


Welcome to ConfigRW documentation!
=====================================

ConfigRW is a simple reader and writer config files based on key-value or INI-structure.

Getting Started
===============

Здесь описать процесс инсталяции

Quick start
===========

In this example we will use the following INI file:

.. code:: ini

    # This is comment
    this is option = this is value
    second option  = -100

    [ SECTION1 ] # comment
        option1 = 100
        option2 = 200
        # comment
        option3 = 1.2

    [ section2 ]
        param1 = 'str'
        param2 = 0 # comment
        parameter_without_value

    [section3]
        extensions =
            # comment1
            ext1
            # comment2
            ext2
            ext3

Access to non-section area
--------------------------

This is features needed if you want use simple key-value of config file

.. code:: python

    from configrw import Config

    config = Config().from_file('./path/to/file')

    section = config[None]             # Getting non-section
    value = section['this is option']  # Getting the value
    section['this is option'] = None   # Setting the value
    del section['second option']       # Deleting the option

Access to section area
----------------------

This is features needed if you want use INI config file

.. code:: python

    value = config['SECTION1']['option2']       # Getting the value
    config['SECTION1']['option2'] = 0           # Setting the value
    config['SECTION1']['option3'] = 300         # Adding new option to section

    config['section3']['extensions'].append('ext4')     # Adding new value to multiple values
    config['section3']['extensions'].insert('ext0', 0)  # Inserting new value
    config['section3']['extensions'][0] = 'extension0'  # Changing single value of multiple values

    config.write('./path/to/file')              # Saving config to file

    # to output config on screen
    for line in config.to_text():
        print(line)

INI-file after changes:

.. code:: ini

    # This is comment
    this is option

    [ SECTION1 ] # comment
        option1 = 100
        option2 = 0
        # comment
        option3 = 300

    [ section2 ]
        param1 = 'str'
        param2 = 0 # comment
        parameter_without_value

    [section3]
        extensions =
            extension0
            # comment1
            ext1
            # comment2
            ext2
            ext3
            ext4

Load config
===========

You can load configuration from file:

.. code:: python

    from configrw import Config

    config = Config().from_file('./path/to/file')

or load config from string:

.. code:: python

    config = Config().from_str("""
    [section1]
    option1 = 100
    option2 = 200

    [section2]
    option1 = 300
    """)

or create new empty config:

.. code:: python

    config = Config()

Management of sections
======================

Checking if has a section
-------------------------

For checking existing section you can use method `has_section()`:

.. code:: python

    if not config.has_section('section1'):
        print('Not exists')

or use iteration:

.. code:: python

    if not 'section1' in config:
        print('Not exists')

Add new section
---------------

Adding a new section or reset exist section:

.. code:: python

    new_section = config.add_section('section1')

Get an section
--------------

Get non-section area for management of simple configs:

.. code:: python

    non_section = config[None]
    non_section = config.get_section()

Also you can get an existing section in two different ways:

.. code:: python

    section1 = config['section1']
    section1 = config.get_section('section1')


if section do not exist then raised ``KeyError``

Remove an section
-----------------

Management of items of section
==============================

Set or add new an option
------------------------

Getting values of option
------------------------

Remove an option
----------------

Add new an item into a section
------------------------------

Get any item in a section by index
----------------------------------

Remove any item from a section by index
---------------------------------------

Print data
==========

Write data to a file
====================
