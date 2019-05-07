.. _sections_doc:

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

Also, you can add new section with a leading spaces or add comment after section name:

.. code:: python

    new_section = config.add_section('section1', text_before='   ', text_after=' # This is comment')

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
