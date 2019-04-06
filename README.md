# configrw

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

section = config[None]             # get non-section
value = section['this is option']  # get value
section['this is option'] = None   # set value
del section['second option']       # delete option
```

### Access to section area

This is features need if you use INI config file

```python
value = config['SECTION1']['option2']       # get value
config['SECTION1']['option2'] = 0           # set value
config['SECTION1']['option3'] = 300         # add new option to section

config['section3']['extensions'].append('ext4')     # add new value to multivalue option
config['section3']['extensions'].insert('ext0', 0)  # insert new value
config['section3']['extensions'][0] = 'extension0'  # change value for multivalue option

config.write('./path/to/file')              # saving config to a file

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
