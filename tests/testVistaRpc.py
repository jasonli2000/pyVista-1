__author__ = 'Joe'

import unittest
from VistaRpc import VistaRpc
from RpcParameter import RpcParameter

class TestVistaRpc(unittest.TestCase):

    def test_disconnect_rpc(self):
        expected = "[XWB]10304\x05#BYE#\x04"
        actual = VistaRpc.prepare('BYE')
        self.assertEqual(expected, actual)

    def test_connect_rpc(self):
        expected = "[XWB]10304\x0ATCPConnect50013192.168.1.107f00010f0022LAPTOP2.v11.med.va.govf\x04"
        params = [
            RpcParameter(RpcParameter.LITERAL, '192.168.1.107'),
            RpcParameter(RpcParameter.LITERAL, 'LAPTOP2.v11.med.va.gov')
        ]
        actual = VistaRpc.prepare('HELLO', params)
        self.assertEqual(expected, actual)

    def test_into_msg_rpc(self):
        expected = "[XWB]11302\x051.108\x0DXUS INTRO MSG54f\x04"
        actual = VistaRpc.prepare('XUS INTRO MSG')
        self.assertEqual(expected, actual)

    def test_setup_login_rpc(self):
        expected = "[XWB]11302\x051.108\x10XUS SIGNON SETUP54f\x04"
        actual = VistaRpc.prepare('XUS SIGNON SETUP')
        self.assertEqual(expected, actual)

    def test_login_rpc(self):
        expected = "[XWB]11302\x051.108\x0BXUS AV CODE50017.r v11k3}!r&sAgP$f\x04"
        param = RpcParameter(RpcParameter.ENCRYPTED, 'ijr773;Akiba12.', [14,4])
        actual = VistaRpc.prepare('XUS AV CODE', [param])
        self.assertEqual(expected, actual)

    def test_set_context_rpc(self):
        expected = "[XWB]11302\x051.108\x12XWB CREATE CONTEXT50019(&y?#jy<?x:=?#68y].f\x04"
        param = RpcParameter(RpcParameter.ENCRYPTED, 'OR CPRS GUI CHART', [8,14])
        actual = VistaRpc.prepare('XWB CREATE CONTEXT', [param])
        self.assertEqual(expected, actual)

    def test_get_variable_value_rpc(self):
        arg = "$P($G(^DIC(3.1,1362,0)),U,1)"
        expected = "[XWB]11302\x051.108\x16XWB GET VARIABLE VALUE51028$P($G(^DIC(3.1,1362,0)),U,1)f\x04"
        param = RpcParameter(RpcParameter.REFERENCE, arg)
        actual = VistaRpc.prepare('XWB GET VARIABLE VALUE', [param])
        self.assertEqual(expected, actual)


