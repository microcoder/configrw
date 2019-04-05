import os
import hashlib
import tempfile
import unittest
from configrw import Config

"""
    For run this test:
        python -m unittest -v tests/tests.py

    DONE: Конфиг может содержать комментарии с префиксом определенных символов, возможно с отступом
    TODO: Имена разделов чувствительны к регистру, а ключи - нет
    TODO: Ведущие и конечные пробелы удаляются из ключей и значений
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

    # @unittest.skip('Temporary skipped')
    def test_02_has_sections(self):

        self.assertTrue(self.config.has_section('SECTION1'))
        self.assertFalse(self.config.has_section('  SECTION1  '))
        self.assertFalse(self.config.has_section('section1'))

        self.assertTrue('SECTION1' in self.config)
        self.assertFalse('  SECTION1  ' in self.config)
        self.assertFalse('section1' in self.config)

    # @unittest.skip('Temporary skipped')
    def test_03_has_options(self):

        self.assertTrue(self.config['section2'].has_option('parameter_without_value'))
        self.assertTrue('parameter_without_value' in self.config['section2'])
        self.assertFalse('param3' in self.config['section2'])

        self.assertTrue(self.config['section3'].has_option('extensions'))
        self.assertTrue('extensions' in self.config['section3'])
        self.assertTrue(self.config['section3'].has_option('option_without_value'))
        self.assertTrue('option_without_value' in self.config['section3'])
        self.assertTrue(self.config['section3'].has_option('another option'))
        self.assertTrue('another option' in self.config['section3'])

        self.assertFalse(self.config['section3'].has_option('none_option'))
        self.assertFalse('none_option' in self.config['section3'])

    # @unittest.skip('Temporary skipped')
    def test_04_check_values(self):

        self.assertEqual(self.config['SECTION1']['option1'], 100)
        self.assertEqual(self.config['SECTION1']['option3'], 1.2)
        self.assertEqual(self.config['section2']['parameter_without_value'], None)
        self.assertEqual(self.config['section3']['another option'], 55555)
        with self.assertRaises(KeyError):
            self.config['section3']['none_option']

    # @unittest.skip('Temporary skipped')
    def test_05_set_option(self):

        self.config['section2'].set_option('param0', 10, ': ', 0)
        self.assertTrue(self.config['section2'].has_option('param0'))
        self.assertEqual(self.config['section2']['param0'], 10)

        self.config['section2'].set_option('param1', 1, position=1)
        self.assertTrue(self.config['section2'].has_option('param1'))
        self.assertEqual(self.config['section2']['param1'], 1)

        self.config['section2']['param2'] = 200
        self.assertTrue(self.config['section2'].has_option('param2'))
        self.assertEqual(self.config['section2']['param2'], 200)

        # separator not should be added with None value
        self.config['section2'].set_option('param3', separator=' == ')
        self.assertTrue(self.config['section2'].has_option('param3'))
        self.assertEqual(self.config['section2']['param3'], None)

        # separator should be added
        self.config['section2'].set_option('param3', '', separator=' == ')
        self.assertTrue(self.config['section2'].has_option('param3'))
        self.assertEqual(self.config['section2']['param3'], '')

        self.config['section2']['param4'] = None
        self.assertTrue(self.config['section2'].has_option('param4'))
        self.assertEqual(self.config['section2']['param4'], None)

        with self.assertRaises(ValueError):
            self.config['SECTION1']['option1'] = True      # invalid type value

    # @unittest.skip('Temporary skipped')
    def test_06_check_value_types(self):

        self.config['section3']['opt_empty'] = ''
        self.assertNotEqual(self.config['section3']['opt_empty'], None)
        self.assertEqual(self.config['section3']['opt_empty'], '')

        self.config['section3']['opt_none_value'] = []
        self.assertEqual(self.config['section3']['opt_none_value'], None)

        # Check int type
        self.config['section3']['opt_int'] = 1000
        self.assertEqual(self.config['section3']['opt_int'], 1000)

        self.config['section3']['opt_int'] = '    2000 '
        self.assertEqual(self.config['section3']['opt_int'], 2000)

        # Check float type
        self.config['section3']['opt_float'] = 0.1
        self.assertEqual(self.config['section3']['opt_float'], 0.1)

        self.config['section3']['opt_float'] = '                   0.2 '
        self.assertEqual(self.config['section3']['opt_float'], 0.2)

    # @unittest.skip('Temporary skipped')
    def test_07_check_multivalues(self):

        list_values = ['val1', ' val2', ' val3']
        self.config['section3']['multival'] = list_values
        list_values.insert(3, 'val4')
        list_values.append('val5')
        self.assertEqual(self.config['section3']['multival'], list_values)
        self.assertEqual(self.config['section3'].get_option('multival')['value'], list_values)
        self.assertEqual(id(self.config['section3']['multival']), id(list_values))  # checking identic

        # print()
        # print(list_values)
        # print(self.config['section3']['multival'])
        # for line in self.config['section3'].to_text():
        #     print(line)

        self.config['section3']['multival'] = []
        self.assertEqual(self.config['section3']['multival'], None)

        extensions = self.config['section3']['extensions']
        extensions.append('ext3')
        # print(extensions)
        # for line in self.config['section3'].to_text():
        #     print(line)

    # @unittest.skip('Temporary skipped')
    def test_08_remove_option(self):

        del self.config['section3']['multival']
        self.assertFalse(self.config['section3'].has_option('multival'))
        self.assertFalse(self.config['section3'].remove_option('multival'))
        with self.assertRaises(KeyError):
            self.config['section3']['multival']

    # @unittest.skip('Temporary skipped')
    def test_09_remove_section(self):

        del self.config['SECTION1']
        self.assertFalse(self.config.has_section('SECTION1'))
        with self.assertRaises(KeyError):
            self.config['SECTION1']

        # None-section cannot be deleted
        del self.config[None]

    # @unittest.skip('Temporary skipped')
    def test_10_write_config(self):

        self.config._filepath = None
        with self.assertRaises(AttributeError):
            self.config.write()  # without filepath specified

        filepath = tempfile.gettempdir() + '/test_config.ini'

        self.config._filepath = filepath
        self.config.write()

        self.config.write(filepath)
        os.unlink(self.config._filepath)

    # @unittest.skip('Temporary skipped')
    def test_11_str_equals(self):
        self.config = Config().from_file('tests/config.ini')
        self.config2 = Config().from_file('tests/config.ini')

        self.assertTrue(self.config == self.config2)

        del self.config2

    # @unittest.skip('Temporary skipped')
    def test_12_text_hash_equals(self):

        hash1 = None
        hash2 = None

        with open('tests/config.ini', 'r') as f:
            hash1 = hashlib.sha3_256(f.read().encode()).hexdigest()

        self.config = Config().from_file('tests/config.ini')
        with open('tests/config_out.ini', 'w') as f:
            for line in self.config.to_text():
                f.writelines(line)

        with open('tests/config_out.ini', 'r') as f:
            hash2 = hashlib.sha3_256(f.read().encode()).hexdigest()

        # print(hashlib.algorithms_guaranteed)
        # print()
        # print(hash1)
        # print(hash2)

        self.assertEqual(hash1, hash2)

    @unittest.skip('Temporary skipped')
    def test_13_examples(self):

        # create new config
        config = Config()

        # get non-section
        section = config[None]

        # set or add new value:
        section['option1'] = 100  # or section.set_option('option2', 100)

        # get value
        value = section['option1']  # or section.get_value('option1')
        print(value)

        # get option
        option1 = section.get_option('option1')
        print(option1)

        # set custom value separator
        option2 = section.set_option('option2', 200, ' : ')
        print(option2)
        print(section['option2'])

        # set custom option position
        section.set_option(key='option3', value=300, separator=' = ', position=0)
        print(section)

        # adding comments or any other entry
        section.add_item(item='', position=0)
        section.add_item(item='# this my first comment', position=1)
        section.add_item('')
        section.add_item({'key': 'mykey', 'separator': ' = ', 'value': 1000})
        section.add_item('')
        print(section)

        # adding multivalue option and set indents
        section['multivalue'] = ['                    one', 'two', '  three', 4, 'five', (100, 200, 300)]
        # or:
        section.set_option('extensions', ['ext1', 'ext2'])

        # print text format
        for i in section.to_text():
            print(i)


if __name__ == '__main__':
    unittest.main()
