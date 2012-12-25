__author__ = 'Joe'

import unittest
from VistaConnection import VistaConnection

class TestVistaConnection(unittest.TestCase):

    def setUp(self):
        self.host = '74.67.137.153'
        self.port = 19200
        self.cxn = VistaConnection(self.host, self.port)

    def test_connect_disconnect(self):
        self.cxn.connect()
        self.assertTrue(self.cxn.is_connected)
        self.cxn.disconnect()
        self.assertFalse(self.cxn.is_connected)

