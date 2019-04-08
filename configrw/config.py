from __future__ import annotations          # forward declaration
from typing import Optional, Iterator, Dict, Any, Union
import os
import re
import io


class ConfigSection():

    DEFAULT_OPT_SEPARATOR = ' = '

    def __init__(self,
                 inline_text: Optional[str] = None,
                 default_opt_separator: str = DEFAULT_OPT_SEPARATOR,
                 convert_values: bool = True
                 ):
        self._inline_text: Optional[str] = inline_text
        self._items: list = []
        self.DEFAULT_OPT_SEPARATOR = default_opt_separator
        self._allowed_types_value = (str, type(None), int, float, list)
        self._convert_values = convert_values

    def __getitem__(self, key: Union[str, int]) -> Any:
        if isinstance(key, str):
            return self.get_value(key)
        return self._items[key]

    def __setitem__(self, key: str, value: Any):
        return self.set_option(key, value)

    def __delitem__(self, key: Union[str, int]) -> None:
        if isinstance(key, str):
            self.remove_option(key)
            return

        del self._items[key]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):

        if self.n < len(self._items):
            self.n += 1

            if isinstance(self._items[self.n - 1], dict):
                return self._items[self.n - 1]['key'].strip()

            return None

        raise StopIteration

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def __repr__(self):
        return str(self._items)

    def add_item(self, item: Union[str, Dict[str, Any]], pos: Optional[int] = None) -> None:
        """Adding a item into the section.

            `pos` = Number position of item. If not specified, it is added to the end of the section.
        """

        if pos is not None:
            self._items.insert(pos, item)
            return

        self._items.append(item)

    def has_option(self, key: str) -> bool:

        for item in self._items:
            if isinstance(item, dict) and item['key'].strip() == key.strip():
                return True

        return False

    def get_option(self, key: str) -> Dict[str, Any]:

        for item in self._items:
            if isinstance(item, dict) and item['key'].strip() == key:
                return item

        raise KeyError(f'Option "{key}" not found')

    def set_option(self, key: str,
                   value: Optional[Union[str, int, float, list]] = None,
                   sep: Optional[str] = DEFAULT_OPT_SEPARATOR,
                   pos: Optional[int] = None) -> Dict[str, Any]:
        """Adding a new option or setting new value of existing option. Returning option"""

        if type(value) not in self._allowed_types_value:
            raise ValueError(f'Value of option must be a type of: {self._allowed_types_value}')

        if value is None:
            sep = None
        elif isinstance(value, list):
            if len(value) == 0:  # if this multiple values
                value = None
                sep = None

        # Searching exists option
        for n, item in enumerate(self._items):
            if isinstance(item, dict) and item['key'].strip() == key.strip():
                item['key'] = key
                item['sep'] = sep
                item['value'] = value
                if pos is not None:    # moving position
                    del self._items[n]
                    self._items.insert(pos, item)
                return item

        # Setting a new option
        new_option = {
            'key': key,              # saving key without applying strip()
            'sep': sep,
            'value': value
        }

        self.add_item(new_option, pos)
        return new_option

    def remove_option(self, key: str) -> bool:
        """Remove the given option from the given section."""

        for i, item in enumerate(self._items, start=0):
            if isinstance(item, dict):
                if item['key'].strip() == key:
                    del self._items[i]
                    return True
            elif item.strip() == key:
                del self._items[i]
                return True

        return False

    def get_value(self, key: str) -> Any:

        if not self._convert_values:
            return self.get_option(key)['value']

        value = self.get_option(key)['value']

        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                pass

            try:
                return int(value)
            except ValueError:
                pass

        return value

    def to_text(self) -> Iterator[str]:
        """The function is generator of output text the section"""

        for item in self._items:
            if item is None:
                yield ''
                continue

            if isinstance(item, dict):
                text = str(item['key'])

                if item['sep'] is not None:
                    text += str(item['sep'])

                if item['value'] is None:
                    yield text
                    continue

                if isinstance(item['value'], list):
                    yield text + ''

                    # default_indent = first_value_indent or key indent + 4 whitespaces:
                    first_value = str(item['value'][0])
                    len_fv_indent = len(first_value) - len(first_value.lstrip())
                    default_indent = first_value[:len_fv_indent] or ' ' * (abs(len(item['key'].lstrip()) - len(item['key'])) + 4)
                    # print(f'default_indent "{default_indent}"')

                    for value in item['value']:
                        value = str(value)
                        if len(value.lstrip()) > 0:  # if value not empty
                            len_current_indent = abs(len(value.lstrip()) - len(value))
                            len_default_indent = len(default_indent)

                            if len_current_indent < len_default_indent:
                                yield default_indent + value
                            elif len_current_indent > len_default_indent:
                                yield default_indent + value[len_default_indent:]
                            else:
                                yield value

                        else:
                            yield value

                    continue

                yield text + str(item['value'])
                continue

            yield str(item)  # output other items


class Config():

    REGEXP_COMMENT = r"""
        (?P<comment>\s*(?:(?P<sep>{sep})).*$)
        """

    REGEXP_SECTION = r"""
        \[
        (?P<name>[^]]+)
        \]
        (?:
            (?P<comment>.*)
        )?$
        """

    REGEXP_OPTION = r"""
        (?P<key>\s*[^\s]+.*?)
        (?:
            (?P<sep>[ \t]*({sep})[ \t]*)
            (?P<value>.*)
        )?$
        """

    def __init__(self, option_sep=('=', ':'), comment_sep=('#', ';'), remove_extra_lines=False,
                 # inline_comment_sep=(';',),
                 # remove_extra_spaces=False,
                 ):

        regexp_option_sep = '|'.join(re.escape(d) for d in option_sep)
        regexp_comment_sep = '|'.join(re.escape(d) for d in comment_sep)

        # Compiled regular expression for matching sections
        self._regexp_comment = re.compile(self.REGEXP_COMMENT.format(sep=regexp_comment_sep), re.VERBOSE)
        self._regexp_section = re.compile(self.REGEXP_SECTION, re.VERBOSE)
        self._regexp_option = re.compile(self.REGEXP_OPTION.format(sep=regexp_option_sep), re.VERBOSE)
        # print('compiled _regexp_option:', self._regexp_option.pattern, sep='\n')

        self._remove_extra_lines = remove_extra_lines
        # self._remove_extra_spaces = remove_extra_spaces

        self._none_section = ConfigSection()
        self._sections = {}

    def __getitem__(self, key):
        return self.get_section(key)

    def __delitem__(self, key):
        return self.remove_section(key)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        sections = list(self._sections.keys())

        if self.n < len(sections):
            self.n += 1
            return sections[self.n - 1].strip()

        raise StopIteration

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return str((self._none_section, self._sections))

    def has_section(self, name: str) -> bool:

        for s in self._sections.keys():
            if s.strip() == name:
                return True

        return False

    def get_section(self, name: Optional[str] = None) -> ConfigSection:

        if name is None:
            return self._none_section

        for s in self._sections.keys():
            if s.strip() == name:
                return self._sections[s]

        raise KeyError(f'Section "{name}" not exists')

    def add_section(self, name, inline_text=None) -> ConfigSection:

        self._sections[name] = ConfigSection(inline_text)

        return self._sections[name]

    def remove_section(self, name: str) -> bool:
        """Remove the given file section and all its options."""

        for s in self._sections.keys():
            if s.strip() == name:
                del self._sections[s]
                return True

        return False

    def _load(self, fp):

        current_section: ConfigSection = self._none_section
        current_option: Optional[Dict[str, Any]] = None     # Needed for multiple values

        for line in fp:

            # --------- Parsing sections
            parsed = self._regexp_section.match(line)
            if parsed is not None:
                current_section = self.add_section(parsed.group('name'), parsed.group('comment'))
                current_option = None
                continue

            # --------- Parsing comments line
            parsed = self._regexp_comment.match(line)
            if parsed is not None:

                parsed_key = parsed.group('comment')

                if current_option is not None:
                    parsed_key_indent = len(parsed_key) - len(parsed_key.lstrip())
                    option_key_indent = len(current_option['key']) - len(current_option['key'].lstrip())

                    if current_option['value'] == '':
                        if parsed_key_indent > option_key_indent:
                            current_option['value'] = [parsed_key]
                            continue
                    elif isinstance(current_option['value'], list):
                        if parsed_key_indent > option_key_indent:
                            current_option['value'].append(parsed_key)
                            continue

                current_section.add_item(parsed_key)
                current_option = None
                continue

            # --------- Parsing options
            parsed = self._regexp_option.match(line)
            if parsed is not None:

                parsed_key = parsed.group('key')
                parsed_sep = parsed.group('sep')
                parsed_value = parsed.group('value')

                if parsed_sep is None:  # if current option without value
                    if current_option is not None:
                        parsed_key_indent = len(parsed_key) - len(parsed_key.lstrip())
                        option_key_indent = len(current_option['key']) - len(current_option['key'].lstrip())

                        if current_option['value'] == '':
                            if parsed_key_indent > option_key_indent:
                                current_option['value'] = [parsed_key]
                                continue
                        elif isinstance(current_option['value'], list):
                            if parsed_key_indent > option_key_indent:
                                current_option['value'].append(parsed_key)
                                continue

                current_option = current_section.set_option(parsed_key, parsed_value, parsed_sep)
                continue

            # --------- Adding empty and unrecognized lines:
            if not self._remove_extra_lines:
                if current_option is not None and isinstance(current_option['value'], list):
                    current_option['value'].append(line.rstrip('\n'))
                    continue

                current_section.add_item(line.rstrip('\n'))
                current_option = None

    def from_file(self, filepath: str) -> 'Config':
        self._filepath = filepath

        with open(filepath, 'r') as fp:
            self._load(fp)

        return self

    def from_str(self, string: str) -> 'Config':
        """Read configuration from a given string."""

        sfile = io.StringIO(string)
        self._load(sfile)

        return self

    def write(self, filepath: Optional[str] = None):

        if filepath is not None:
            self._filepath = filepath
        elif not hasattr(self, '_filepath') or self._filepath is None:
            raise AttributeError('No filepath specified')

        file_suffix = '.new'  # For safe file writing

        with open(self._filepath + file_suffix, 'w') as fp:
            for option in self._none_section.to_text():
                print(option, file=fp)
            for section_name, section in self._sections.items():
                print(f'[{section_name}]', file=fp)
                for option in section.to_text():
                    print(option, file=fp)

        if os.path.isfile(self._filepath + file_suffix):
            os.rename(self._filepath + file_suffix, self._filepath)

    def to_text(self):

        for line in self._none_section.to_text():
            yield line

        for section_name, section in self._sections.items():
            yield f"[{section_name}]{section._inline_text or ''}"
            for line in section.to_text():
                yield line
