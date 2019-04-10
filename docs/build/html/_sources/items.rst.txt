.. _items_doc:

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

Instead of using ``set_option()`` method, you can use the low-level
method ``add_item()`` to add empty lines, comments to the section:

.. code:: python

    # append new option:
    section1.add_item({'key': '    option2', 'sep': ' = ', 'value': 2})
    # insert new option
    section1.add_item({'key': '    option0', 'sep': ' = ', 'value': 0}, pos=0)
    # insert empty line
    section1.add_item('', pos=0)
    # append empty line
    section1.add_item('')
    # insert comment
    section1.add_item('    # This is comment for option1', 3)

Result:

.. code:: ini

    global_parameter = 1
    [section1] # this is comment

        option0 = 0
        option_without_value
        # This is comment for option1
        option1 = 100
        option2 = 2

Get an item by index
--------------------
.. code:: python

    comment = section1[3]
    option1_value = section1[4]['value']
    last_item = section1[len(section1) - 1]

Remove an item by index
-----------------------
.. code:: python

    del section1[0]
    del section1[5]
    del section1[4]

Result:

.. code:: ini

    global_parameter = 1
    [section1] # this is comment
        option0 = 0
        option_without_value
        # This is comment for option1
        option1 = 100
