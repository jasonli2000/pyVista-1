__author__ = 'Joe'

from VistaException import VistaException
from RpcParameter import RpcParameter
from VistaRpc import VistaRpc

class VistaUser(object):

    def login(self, cxn, access_code, verify_code, context=None):
        rpc = VistaRpc.prepare('XUS SIGNON SETUP')
        response = cxn.execute(rpc)
        if response is None:
            raise VistaException('Unable to setup login')
        param = [RpcParameter(RpcParameter.ENCRYPTED, access_code + ';' + verify_code)]
        rpc = VistaRpc.prepare('XUS AV CODE', param)
        response = cxn.execute(rpc)
        if response is None:
            raise VistaException('No response to login request')
        greeting = self.load(response)
        self.access_code = access_code
        self.verify_code = verify_code

        if context is not None:
            self.set_context(cxn, context)

        return greeting

    def set_context(self, cxn, context):
        param = [RpcParameter(RpcParameter.ENCRYPTED, context)]
        rpc = VistaRpc.prepare('XWB CREATE CONTEXT', param)
        response = cxn.execute(rpc)
        if response != '1':
            raise VistaException(response)
        self.context = context

    def load(self, response):
        parts = response.split("\r\n")
        if parts[0] == '0':
            raise VistaException(parts[3])
        self.duz = parts[0]
        if len(parts) > 7:
            return parts[7]
        return 'OK'