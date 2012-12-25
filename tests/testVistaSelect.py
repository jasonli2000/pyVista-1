__author__ = 'Joe'

import unittest
from VistaException import VistaException
from VistaSelect import VistaSelect

class TestVistaSelect(unittest.TestCase):

    def setUp(self):
        self.query = VistaSelect()

    def test_set_file(self):
        self.query.file = '200'
        self.assertEqual('200', self.query.file)

    def test_set_iens(self):
        with self.assertRaises(VistaException) as context:
            self.query.iens = 'a'
        e = context.exception
        self.assertEqual('Invalid IENS', e.message)

        with self.assertRaises(VistaException) as context:
            self.query.iens = '67,,'
        e = context.exception
        self.assertEqual('Invalid IENS', e.message)

        with self.assertRaises(VistaException) as context:
            self.query.iens = ',,67,'
        e = context.exception
        self.assertEqual('Invalid IENS', e.message)

        with self.assertRaises(VistaException) as context:
            self.query.iens = '67,,4,'
        e = context.exception
        self.assertEqual('Invalid IENS', e.message)

        self.query.iens = '67'
        self.assertEqual(',67,', self.query.iens)

        self.query.iens = ',67'
        self.assertEqual(',67,', self.query.iens)

        self.query.iens = ',67,'
        self.assertEqual(',67,', self.query.iens)

        self.query.iens = '67,44'
        self.assertEqual(',67,44,', self.query.iens)

        self.query.iens = ',67,44'
        self.assertEqual(',67,44,', self.query.iens)

        self.query.iens = '67,44,'
        self.assertEqual(',67,44,', self.query.iens)

        self.query.iens = ',67,44'
        self.assertEqual(',67,44,', self.query.iens)

    def test_set_fields(self):
        self.query.fields = ''
        self.assertEqual('@', self.query.fields)

        self.query.fields = '@'
        self.assertEqual('@', self.query.fields)

        self.query.fields = '.01;2;4;5;.141;8;9;11;29'
        self.assertEqual('@;.01;2;4;5;.141;8;9;11;29', self.query.fields)

        self.query.fields = '@;.01;2;4;5;.141;8;9;11;29'
        self.assertEqual('@;.01;2;4;5;.141;8;9;11;29', self.query.fields)


    def test_set_flags(self):
        self.query.flags = None
        self.assertEquals('IP', self.query.flags)

        self.query.flags = ''
        self.assertEqual('IP', self.query.flags)

        with self.assertRaises(VistaException) as context:
            self.query.flags = 'I'
        e = context.exception
        self.assertEqual('Current version does packed queries only', e.message)

        self.query.flags = 'BIP'
        self.assertEqual('BIP', self.query.flags)

    def test_prepare_param_list(self):
        self.query.file = '200'
        self.query.fields = '.01;2;4;5;.141;8;9;11;29'
        self.query.number = 1
        self.query.frum = '546'

        expected = [
            ('"FILE"', '200'),
            ('"FIELDS"', '@;.01;2;4;5;.141;8;9;11;29'),
            ('"FLAGS"', 'IP'),
            ('"MAX"', '1'),
            ('"FROM"', '545'),
            ('"XREF"', '#')
        ]
        self.query._VistaSelect__prepare_param_list()
        self.assertEqual(expected, self.query.param_list)


    def test_prepare(self):
        self.query.file = '200'
        self.query.fields = '.01;2;4;5;.141;8;9;11;29'
        self.query.number = 1
        self.query.frum = '546'

        expected = "[XWB]11302\x051.108\x0ADDR LISTER52006\"FILE\"003200t008\"FIELDS\"026@;.01;2;4;5;.141;8;9;11;29t007\"FLAGS\"002IPt005\"MAX\"0011t006\"FROM\"003545t006\"XREF\"001#f\x04"

        self.query._VistaSelect__prepare()
        self.assertEqual(expected, self.query.rpc)

    def test_load(self):
        response = "[Misc]\r\nMORE^546^546^\r\n[MAP]\r\nIEN^.01I^2I^4I^5I^.141I^8I^9I^11I^29I\r\n[BEGIN_diDATA]\r\n546^ZZPROGRAMMER,NINE^@Jy$9BO\'9iCm#:x*p:\'E^F^^^2^666948848^tHffxTgZ)<4~.7`EUx}j^1043\r\n[END_diDATA]"
        expected = [
            ['546','ZZPROGRAMMER,NINE',"@Jy$9BO'9iCm#:x*p:'E",'F','','','2','666948848',"tHffxTgZ)<4~.7`EUx}j",'1043']
        ]
        actual = self.query._VistaSelect__load(response)
        self.assertEqual(expected, actual)
        self.assertEqual(expected, self.query.records)
