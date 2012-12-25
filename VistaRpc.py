__author__ = 'Joe'

from VistaUtils import VistaUtils
from RpcParameter import RpcParameter
from VistaException import VistaException

class VistaRpc(object):

    PREFIX = '[XWB]'
    COUNT_WIDTH = 3
    RPC_VERSION = '1.108'
    EOT = "\x04"

    @staticmethod
    def prepare(rpc_name, params=None):
        if rpc_name == 'HELLO':
            return VistaRpc.__connect_rpc(params)
        if rpc_name == 'BYE':
            return VistaRpc.__disconnect_rpc()
        return VistaRpc.prepare_standard_rpc(rpc_name, VistaRpc.prepare_param_str(params))

    @staticmethod
    def prepare_standard_rpc(rpc_name, param_string):
        return VistaRpc.PREFIX + '11302' + VistaUtils.prepend_count(VistaRpc.RPC_VERSION) + \
                VistaUtils.prepend_count(rpc_name) + param_string + VistaRpc.EOT


    @staticmethod
    def prepare_param_str(params):
        param_str = '5'
        if params:
            for param in params:
                if param.type == RpcParameter.LITERAL:
                    param_str += '0' + VistaUtils.str_pack(param.value, VistaRpc.COUNT_WIDTH) + 'f'
                elif param.type == RpcParameter.REFERENCE:
                    param_str += '1' + VistaUtils.str_pack(param.value, VistaRpc.COUNT_WIDTH) + 'f'
                elif param.type == RpcParameter.LIST:
                    param_str += '2' + RpcParameter.list_to_string(param.value)
                else:
                    raise VistaException('Invalid param type')
        if param_str == '5' : param_str += '4f'
        return param_str

    @staticmethod
    def __connect_rpc(params):
        return "[XWB]10304\x0ATCPConnect50" + VistaUtils.str_pack(params[0].value, VistaRpc.COUNT_WIDTH) + \
                "f0" + VistaUtils.str_pack('0', VistaRpc.COUNT_WIDTH) + \
                "f0" + VistaUtils.str_pack(params[1].value, VistaRpc.COUNT_WIDTH) + \
                "f" + VistaRpc.EOT

    @staticmethod
    def __disconnect_rpc():
        return "[XWB]10304\x05#BYE#" + VistaRpc.EOT
