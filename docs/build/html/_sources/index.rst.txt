

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

For checking existing section you can use method ``has_section()``:

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

.. note::
    if section do not exist then raised ``KeyError``

Remove an section
-----------------

.. code:: python

    del config['section1']

or

.. code:: python

    config.remove_section('section1')

Management of items of section
==============================

Set or add new an option
------------------------

.. code:: python

    section1 = config.add_section('section1', inline_text=' # this is comment')

    section1['option1'] = 'value1'
    section1['option_without_value'] = None
    section1.set_option('option2', 200)

or you can adding option with custom separator or position:

.. code:: python

    section1.set_option('option1', 100, sep=' == ', pos=0)
    section1.set_option('option_without_value', pos=0)

Result:

.. code:: ini

    [section1] # this is comment
    option_without_value
    option1 == 100
    option2 = 200

Also, you can set option to non-section area:

.. code:: python

    non_section = config[None]
    non_section['global_parameter'] = 1

Result:

.. code:: ini

    global_parameter = 1
    [section1] # this is comment
    option_without_value
    option1 == 100
    option2 = 200

You can set option with custom indentation:

.. code:: python

    section1['    option1'] = 100
    section1.set_option('    option1', 100)

    section1['    option_without_value'] = None
    section1.set_option('    option_without_value')

Result:

.. code:: ini

    global_parameter = 1
    [section1] # this is comment
        option_without_value
        option1 = 100
    option2 = 200

Get values of option
------------------------

You can get an option value in three different ways:

.. code:: python

    value = section1['option1']
    value = section1.get_value('option1')
    value = section1.get_option('option1')['value']

.. note::
    Also you can get value by index at section. See the chapter next.

Remove an option
----------------

.. code:: python

    del section1['option2']

or

.. code:: python

    section1.remove_option('option2')

.. note::
    Also you can delete an option by index. See the chapter next.

Add a new item
--------------

Get an item by index
--------------------

Remove an item by index
-----------------------

Print data
==========

Write data to a file
====================
