.. _print_doc:

Print data
==========

.. code:: python

    print(config)

Output:

.. code:: python

    [
        {'key': 'global_parameter', 'sep': ' = ', 'value': 1}
    ], 
    {'section1': 
        [
            {'key': '    option0', 'sep': ' = ', 'value': 0},
            {'key': '    option_without_value', 'sep': None, 'value': None},
            '    # This is comment for option1',
            {'key': '    option1', 'sep': ' = ', 'value': 100}
        ]
    }

.. code:: python

    print(config['section1'])

Output:

.. code:: python

    [
        {'key': '    option0', 'sep': ' = ', 'value': 0},
        {'key': '    option_without_value', 'sep': None, 'value': None},
        '    # This is comment for option1',
        {'key': '    option1', 'sep': ' = ', 'value': 100}
    ]

Also you can use method ``to_text()`` for all config or for a section:

.. code:: python

    for line in config.to_text():
        print(line)

Output as text format:

.. code:: ini

    global_parameter = 1
    [section1] # this is comment
        option0 = 0
        option_without_value
        # This is comment for option1
        option1 = 100
