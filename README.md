# ConfigRW
**ConfigRW** is a simple reader and writer config files based on key-value or INI-structure.

    * Максимально сохраняет форматирование исходного файла (отступы, пробелы, комментарии, etc)

# Quick start

```ini
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
```

## Access to non-section area

This is features needed if you want use simple key-value of config file

```python
from configrw import Config

config = Config().from_file('./path/to/file')

section = config[None]             # Getting non-section
value = section['this is option']  # Getting the value
section['this is option'] = None   # Setting the value
del section['second option']       # Deleting the option
```

## Access to section area

This is features needed if you want use INI config file

```python
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
```

INI-file after changes:

```ini
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
```

# Manual

You can load configuration from file:

```python
from configrw import Config

config = Config().from_file('./path/to/file')
```

or load config from string:

```python
config = Config().from_str("""
[section1]
option1 = 100
option2 = 200

[section2]
option1 = 300
""")
```

or create new empty config:

```python
config = Config()
```

## Management of sections

### Checking if has a section

```python
if not config.has_section('section1'):
    print('Not exists')
```

or

```python
if not 'section1' in config:
    print('Not exists')
```

### Add new section

Adding or replaced exists section:

```python
new_section = config.add_section('section1')
```

### Get an section

Get non-section area for management of simple configs:

```python
non_section = config[None]
non_section = config.get_section()
```
or you can get exist section

```python
section1 = config['section1']
section1 = config.get_section('section1')
```

if section do not exist then raised `KeyError`

### Remove an section

```python
del config['section1']
```

or

```python
config.remove_section('section1')
```

## Management of items of section

### Set or add new an option

```python
section1 = config.add_section('section1', inline_text=' # this is comment')
section1['option1'] = 'value1'
section1['option_without_value'] = None
section1.set_option('option2', 200)
```

or you can adding option with custom separator or position:

```python
section1.set_option('option1', 100, sep=' == ', pos=0)
section1.set_option('option_without_value', pos=0)
```

Result:

```ini
[section1] # this is comment
option_without_value
option1 == 100
option2 = 200
```

Also, you can set option to non-section area:

```python
non_section = config[None]
non_section['global_parameter'] = 1
```

Result:

```ini
global_parameter = 1
[section1] # this is comment
option_without_value
option1 == 100
option2 = 200
```

You can set option with custom indentation:

```python
section1['    option1'] = 100
section1.set_option('    option1', 100)

section1['    option_without_value'] = None
section1.set_option('    option_without_value')
```

Result:

```ini
global_parameter = 1
[section1] # this is comment
    option_without_value
    option1 = 100
option2 = 200
```

### Getting values of option

You can get an option value in three different ways:

```python
value1 = section1['option_without_value']         # None
value2 = section1.get_option('option1')['value']  # 100
value3 = section1.get_value('option2')            # 200
```

Also you can get value by index at section. See chapter below.

### Remove an option

```python
del section1['option2']
```

or

```python
section1.remove_option('option2')
```

Also you can delete an option by index. See chapter below.

### Add new an item into a section

Instead of using `set_option()` method, you can use the low-level method `add_item()` to add empty lines, comments to the section

```python
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
```

Result:

```ini
global_parameter = 1
[section1] # this is comment

    option0 = 0
    option_without_value
    # This is comment for option1
    option1 = 100
    option2 = 2

```

### Get any item in a section by index

```python
comment = section1[3]
option1_value = section1[4]['value']
```

### Remove any item from a section by index

```python
del section1[0]
del section1[5]
del section1[4]
```

Result:

```ini
global_parameter = 1
[section1] # this is comment
    option0 = 0
    option_without_value
    # This is comment for option1
    option1 = 100
```

## Print data

```python
print(config)
```
Output:

```python
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
```

```python
print(config['section1'])
```

Output:

```python
[
    {'key': '    option0', 'sep': ' = ', 'value': 0},
    {'key': '    option_without_value', 'sep': None, 'value': None},
    '    # This is comment for option1',
    {'key': '    option1', 'sep': ' = ', 'value': 100}
]
```

Also you can use method `to_text()` for all config or for a section:

```python
for line in config.to_text():
    print(line)
```

Output as text format:

```ini
global_parameter = 1
[section1] # this is comment
    option0 = 0
    option_without_value
    # This is comment for option1
    option1 = 100
```

## Write data to a file

```python
config.write('path/to/file')
```

Else if file was opened, then method `write()` can be call without parameter:

```python
config.write()
```
