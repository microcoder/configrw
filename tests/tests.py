import os
import hashlib
import tempfile
import unittest
from configrw import Config

"""
    For run this test:
        python -m unittest -v tests/tests.py

    DONE: Конфиг может содержать комментарии с префиксом определенных символов, возможно с отступом
    DONE: Ведущие и конечные пробелы удаляются из ключей и значений
    DONE: Значения могут быть опущены, и в этом случае разделитель ключ/значение также может быть пропущен
    DONE: Значения могут занимать несколько строк, если они имеют тот же отступ или глубже, чем первая строка значения
    DONE: Вставка опции на произвольном номере строки в секции
    DONE: Доступ к значению: config['section']['option']
    DONE: Итератор: for option in config['section']
    DONE: Safe writing to a file. При записи конфига в файл, старый конфиг переименовывается в *.bak файл (backup),
            а когда файл будет успешно записан, *.bak файл удаляется
    TODO: Перед чтением конфига нужно получить его HASH и хранить до записи. При записи проверить, если изменился HASH,
            значит кто-то изменил конфиг пока мы работали с ним в памяти. Выдать предупреждение или выкинуть Exception
    TODO: оформить как у конкурента - https://pypi.org/project/iniconfig/
"""


# @unittest.skip('Skip ConfigTests')
class ConfigTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.config = Config().from_file('tests/config.ini')

    # You can use next decorators for methods:
    #   @unittest.skip('Temporary skipped')
    #   @unittest.skipIf(condition, reason)
    #   @unittest.skipUnless(condition, reason)
    #   @unittest.expectedFailure

    # @unittest.skip('Temporary skipped')
    def test_01_none_section(self):

        none_section = self.config[None]
        none_section = self.config.get_section()

        self.assertTrue(none_section.has_option('this is option'))
        self.assertEqual(none_section['this is option'], 'this is value   ')
        self.assertEqual(none_section['second option'], -10000000000)

        # changing existing option value
        none_section['second option'] = 100
        self.assertEqual(none_section['second option'], 100)

        # adding new option
        none_section['option3'] = 300
        self.assertEqual(none_section['option3'], 300)

        # adding new option without value
        none_section['option4'] = None
        self.assertEqual(none_section['option4'], None)

    def test_02_sections(self):

        self.assertFalse(self.config.has_section('SECTION'))
        self.assertTrue(self.config.has_section('SECTION1'))
        self.assertFalse(self.config.has_section('  SECTION1  '))
        self.assertFalse(self.config.has_section('section1'))

        self.assertTrue('SECTION1' in self.config)
        self.assertFalse('  SECTION1  ' in self.config)
        self.assertFalse('section1' in self.config)

        # get section
        section1 = self.config['SECTION1']
        section1 = self.config.get_section('SECTION1')
        del section1  # remove only link to the section

        # adding new section
        newsection = self.config.add_section('new-section')
        self.assertTrue(self.config.has_section('new-section'))
        del newsection  # remove only link to the section

    def test_03_options(self):

        section2 = self.config['section2']
        section3 = self.config['section3']

        # check option
        self.assertTrue(section2.has_option('param_without_value'))
        self.assertTrue('param_without_value' in section2)
        self.assertFalse('param3' in section2)
        self.assertTrue(section3.has_option('extensions'))
        self.assertTrue('extensions' in section3)
        self.assertTrue(section3.has_option('option_without_value'))
        self.assertTrue('option_without_value' in section3)
        self.assertFalse(section3.has_option('none option'))
        self.assertFalse('none option' in section3)

        # set new option
        section2['param0'] = 0
        self.assertTrue(section2.has_option('param0'))
        self.assertEqual(section2['param0'], 0)

        # reset option
        section2.set_option('param0', 10, ': ', 0)
        self.assertTrue(section2.has_option('param0'))
        self.assertEqual(section2['param0'], 10)

        # moving position of param1
        section2.set_option('param1', 1, pos=0)
        self.assertTrue(section2.has_option('param1'))
        self.assertEqual(section2['param1'], 1)

        # setting parameter without value with custom indent
        section2['    param2_without_value'] = None
        self.assertTrue(section2.has_option('param2_without_value'))
        self.assertEqual(section2['param2_without_value'], None)

        # separator not should be added with non-value
        section2.set_option('param2', sep=' == ')
        self.assertTrue(section2.has_option('param2'))
        self.assertEqual(section2.get_option('param2')['sep'], None)
        self.assertEqual(section2.get_option('param2')['value'], None)

        # separator should be added
        section2.set_option('param2', '', sep=' == ')
        self.assertTrue(section2.has_option('param2'))
        self.assertEqual(section2.get_option('param2')['sep'], ' == ')
        self.assertEqual(section2.get_option('param2')['value'], '')

        with self.assertRaises(ValueError):
            self.config['SECTION1']['option1'] = True  # invalid set type value

        with self.assertRaises(KeyError):
            section2['none_option']

        # remove options
        del section2['param0']
        self.assertFalse(section2.has_option('param0'))
        self.assertFalse(section2.remove_option('param0'))
        with self.assertRaises(KeyError):
            section2['param0']

        # print()
        # for line in section2.to_text():
        #     print(line)

    def test_04_values(self):

        section1 = self.config['SECTION1']
        section2 = self.config['section2']
        section3 = self.config['section3']

        self.assertEqual(section2['param_without_value'], None)
        self.assertEqual(section3['another option'], 55555)

        section3['option_empty'] = ''
        self.assertNotEqual(section3.get_option('option_empty')['sep'], None)
        self.assertNotEqual(section3['option_empty'], None)
        self.assertEqual(section3['option_empty'], '')

        section3['option_none_value'] = []
        self.assertEqual(section3.get_option('option_none_value')['sep'], None)
        self.assertEqual(section3['option_none_value'], None)

        # Check int type
        self.assertEqual(section1['option1'], 100)
        section3['option_int'] = 1000
        self.assertEqual(section3['option_int'], 1000)
        section3['option_int'] = '    1000 '
        self.assertEqual(section3['option_int'], 1000)

        # Check float type
        self.assertEqual(section1['option3'], 1.2)
        section3['option_float'] = 0.1
        self.assertEqual(section3['option_float'], 0.1)
        section3['option_float'] = '        0.2 '
        self.assertEqual(section3['option_float'], 0.2)

    def test_05_multiple_values(self):

        section3 = self.config['section3']
        list_values = ['val1', ' val2', ' val3']

        # set new option
        section3['multiple'] = list_values
        self.assertEqual(section3['multiple'], list_values)

        # adding values
        list_values.insert(3, 'val4')
        list_values.append('val5')

        # checking identic
        self.assertEqual(section3['multiple'], list_values)
        self.assertEqual(id(section3['multiple']), id(list_values))

        # adding new value
        extensions = section3['extensions']
        extensions.append('ext3')

        # print(extensions)
        # print()
        # for line in section3.to_text():
        #     print(line)

    def test_06_remove_sections(self):

        del self.config['new-section']
        self.assertFalse(self.config.has_section('new-section'))

        self.config.remove_section('SECTION1')
        self.assertFalse(self.config.has_section('SECTION1'))
        with self.assertRaises(KeyError):
            self.config['SECTION1']

        # non-section cannot be deleted
        del self.config[None]

    def test_07_items(self):

        section2 = self.config['section2']
        comment = section2[0]
        param2_value = section2[2]['value']
        count_items = len(section2)

        del comment
        del param2_value
        del count_items

    def test_08_write_config(self):

        self.config._filepath = None
        with self.assertRaises(AttributeError):
            self.config.write()  # without filepath specified

        filepath = tempfile.gettempdir() + '/test_config.ini'

        self.config._filepath = filepath
        self.config.write()

        self.config.write(filepath)
        os.unlink(self.config._filepath)

    def test_09_str_equals(self):
        self.config = Config().from_file('tests/config.ini')
        self.config2 = Config().from_file('tests/config.ini')

        self.assertTrue(self.config == self.config2)

    def test_10_hash_equals(self):

        hash1 = None
        hash2 = None

        with open('tests/config.ini', 'r') as f:
            hash1 = hashlib.sha3_256(f.read().encode()).hexdigest()

        self.config = Config().from_file('tests/config.ini')
        filetmp = tempfile.gettempdir() + '/test_config.ini'
        with open(filetmp, 'w') as f:
            for line in self.config.to_text():
                f.write(line + '\n')

        with open(filetmp, 'r') as f:
            hash2 = hashlib.sha3_256(f.read().encode()).hexdigest()

        os.unlink(filetmp)

        # print(hashlib.algorithms_guaranteed)
        # print(hash1)
        # print(hash2)

        self.assertEqual(hash1, hash2)

    def test_11_user_manual(self):

        config = Config()
        section1 = config.add_section('section1', inline_text=' # this is comment')
        section1['option1'] = 'value1'
        section1['option_without_value'] = None
        section1.set_option('option2', 200)

        section1.set_option('option1', 100, sep=' == ', pos=0)
        section1.set_option('option_without_value', pos=0)

        non_section = config[None]
        non_section['global_parameter'] = 1

        section1.set_option('    option1', 100)
        section1.set_option('    option_without_value')

        value = section1['option_without_value']
        value = section1.get_option('option1')['value']
        value = section1.get_value('option2')

        del section1['option2']
        # section1.remove_option('option2')

        # Add new items
        section1.add_item({'key': '    option2', 'sep': ' = ', 'value': 2})
        section1.add_item({'key': '    option0', 'sep': ' = ', 'value': 0}, pos=0)
        section1.add_item('', pos=0)
        section1.add_item('')
        section1.add_item('    # This is comment for option1', 3)

        # Get items
        value = section1[4]['value']
        comment = section1[1]['value']
        last_item = section1[len(section1) - 1]
        del value
        del comment
        del last_item

        # Remove items
        del section1[0]
        del section1[5]
        del section1[4]

        # print()
        # for line in config.to_text():
        #     print(line)

        # print()
        # for line in config.to_text():
        #     print(line)


if __name__ == '__main__':
    unittest.main()
