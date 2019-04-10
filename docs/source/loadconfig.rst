.. _loadconfig_doc:

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
