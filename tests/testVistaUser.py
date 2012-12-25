__author__ = 'Joe'

import unittest
from VistaConnection import VistaConnection
from VistaUser import VistaUser

class TestVistaUser(unittest.TestCase):

    def setUp(self):
        self.host = '74.67.137.153'
        self.port = 19200
        self.cxn = VistaConnection(self.host, self.port)

    def test_login(self):
        self.cxn.connect()
        self.assertTrue(self.cxn.is_connected)

        user = VistaUser()
        access_code = '1programmer'
        verify_code = 'programmer1.'
        context = 'OR CPRS GUI CHART'
        greeting = user.login(self.cxn, access_code, verify_code, context)
        self.cxn.disconnect()

        self.assertEqual(access_code, user.access_code)
        self.assertEqual(verify_code, user.verify_code)
        self.assertEqual(context, user.context)
        self.assertEqual('1', user.duz)
        self.assertTrue(greeting.find('ZZPROGRAMMER'))

