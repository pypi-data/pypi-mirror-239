from __future__ import annotations
import tempfile
import unittest
import logging
#import io
#import sys
#import time

#from console import Console, color_numbers
from properties import Properties
class PropertiesTest(unittest.TestCase):
    TEST_MESSAGE = 'TEST MESSAGE'

    TESTDATA: dict[str, str] = {
        'test_bool_false_number': '0',
        'test_bool_true_yes': 'yes',
        'test_bool_false_nei': 'nei',
        'test_bool_true_true': 'true',
        'test_bool_false_usann': 'usann',
        'test_lvl_debug': 'debug',
        'test_lvl_info': 'INFO',
        'test_lvl_warning': 'warning',
        'test_lvl_error': 'ErrOR',
        'test_lvl_critical': 'cRITICAL',
        'test_int_zero': '0',
        'test_int_neg1': '-1',
        'test_int_neg32bit': '-2147483646',
        'test_int_pos1': '1',
        'test_int_pos32bit': '2147483647',
        'test_str_ascii': 'Hello World',
        'test_str_utf8': 'Hælla på dæ',
        'test_str_snowman': '☃'
    }

    DATA = '''#Commentet line 1
# Commented line 2
## ## Commented line 3
test_boolean_true_number=1
test_bool_false_number=0
test_bool_true_yes=yes
test_bool_false_nei=nei
test_bool_true_true=true
test_bool_false_usann=usann
test_lvl_debug=debug
test_lvl_info=INFO
test_lvl_warning=warning
test_lvl_error=ErrOR
test_lvl_critical=cRITICAL
test_int_zero=0
test_int_neg1=-1
test_int_neg32bit=-2147483646
test_int_pos1=1
test_int_pos32bit=2147483647
test_str_ascii=Hello World
test_str_utf8=Hælla på dæ
test_str_snowman=☃'''

    properties_file: tempfile._TemporaryFileWrapper = None
    properties: Properties = None

    @classmethod
    def setUpClass(cls) -> None:
        super(PropertiesTest, cls).setUpClass()
        cls.properties_file = tempfile.NamedTemporaryFile(delete=False)
        cls.properties_file.write(b'# Comment')
        cls.properties_file.close()
        with open(cls.properties_file.name, mode='w') as f:
            f.write(cls.DATA)
        cls.properties = Properties(cls.properties_file.name)
  
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.properties_file.delete = True
        pass

    def test_get_bol(self) -> None:
        # test_bool_false_number=0
        # test_bool_true_yes=yes
        # test_bool_false_nei=nei
        # test_bool_true_true=true
        # test_bool_false_usann=usann
        false_number: bool = not self.properties.get_bol('test_bool_false_number', True)
        true_yes: bool = self.properties.get_bol('test_bool_true_yes', False)
        false_nei: bool = not self.properties.get_bol('test_bool_false_nei', True)
        true_true: bool = self.properties.get_bol('test_bool_true_true', False)
        false_usann: bool = not self.properties.get_bol('test_bool_false_usann', True)
        assert false_number and true_yes and false_nei and true_true and false_usann

    def test_get_lvl(self) -> None:
        # test_lvl_debug=debug
        # test_lvl_info=INFO
        # test_lvl_warning=warning
        # test_lvl_error=ErrOR
        # test_lvl_critical=cRITICAL
        lvl_debug: bool = logging.DEBUG == self.properties.get_lvl('test_lvl_debug')
        lvl_info: bool = logging.INFO == self.properties.get_lvl('test_lvl_info')
        lvl_warning: bool = logging.WARNING == self.properties.get_lvl('test_lvl_warning')
        lvl_error: bool = logging.ERROR == self.properties.get_lvl('test_lvl_error')
        lvl_critical: bool = logging.CRITICAL == self.properties.get_lvl('test_lvl_critical')
        assert lvl_debug and lvl_info and lvl_warning and lvl_error and lvl_critical

    def test_get_int(self) -> None:
        # test_int_zero=0
        # test_int_neg1=-1
        # test_int_neg32bit=-2147483646
        # test_int_pos1=1
        # test_int_pos32bit=2147483647
        int_zero: bool = self.properties.get_int('test_int_zero') == 0
        int_neg1: bool = self.properties.get_int('test_int_neg1') == -1
        int_neg32bit: bool = self.properties.get_int('test_int_neg32bit') == -2147483646
        int_pos1: bool = self.properties.get_int('test_int_pos1') == 1
        int_pos32bit: bool = self.properties.get_int('test_int_pos32bit') == 2147483647
        assert int_zero and int_neg1 and int_neg32bit and int_pos1 and int_pos32bit

    def test_get_str(self) -> None:
        # test_str_ascii=Hello World
        # test_str_utf8=Hælla på dæ
        # test_str_snowman=☃
        str_ascii: bool = self.properties.get_str('test_str_ascii') == 'Hello World'
        str_utf8: bool = self.properties.get_str('test_str_utf8') == 'Hælla på dæ'
        str_snowman: bool = self.properties.get_str('test_str_snowman') == '☃'
        assert str_ascii and str_utf8 and str_snowman

    def test_iterator(self) -> None:
        ass = True
        # pkeys = self.properties.keys()
        # print(pkeys)
        n : int = -1
        for key in self.properties:
            n += 1
            # print(f"n={n} key={key}")
            if not list(self.properties.keys())[n] == key:
                ass = False # pragma: no cover
        item_list:list = list(self.properties.items())
        print(f"Item count: {len(item_list)}")
        if not len(item_list) == 19:
            ass = False # pragma: no cover
        testitem = self.properties['test_str_snowman']
        if not testitem == '☃':
            ass = False # pragma: no cover
        print(f"testitem:{testitem}")
        last_value = ''
        for value in self.properties.values():
            last_value = value
        if not last_value == '☃':
            ass = False # pragma: no cover
        assert ass

if __name__=='__main__':
	unittest.main()     # pragma: no cover

