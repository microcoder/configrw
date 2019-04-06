# ConfigRW

## Quick start

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

### Access to non-section area

This is features need if you use simple key-value config file

```python
config = Config().from_file('./path/to/file')

section = config[None]             # Getting non-section
value = section['this is option']  # Getting the value
section['this is option'] = None   # Setting the value
del section['second option']       # Deleting the option
```

### Access to section area

This is features need if you use INI config file

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
