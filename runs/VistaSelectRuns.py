__author__ = 'Joe'

import unittest
from VistaConnection import VistaConnection
from RpcParameter import RpcParameter
from VistaRpc import VistaRpc
from VistaUser import VistaUser
from VistaSelect import VistaSelect

class VistaSelectRuns(unittest.TestCase):

    def setUp(self):
        self.host = '74.67.137.153'
        self.port = 19200
        self.cxn = VistaConnection(self.host, self.port)
        self.user = VistaUser()

    def test_fms_run(self):
        query = VistaSelect()
        query.file = '410'
        query.fields = '.01;1;24;23;22'
        query.number = 200
        query.frum = '178'
        query.part = '178'
        query.index = 'AN'

        self.cxn.connect()
        greeting = self.user.login(self.cxn, '1programmer', 'programmer1.', 'DVBA CAPRI GUI')
        rs = query.find(self.cxn)
        self.cxn.disconnect()

        self.assertEqual(56, len(rs))
