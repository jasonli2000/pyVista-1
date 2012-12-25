__author__ = 'Joe'

from VistaException import VistaException
from VistaUtils import VistaUtils
from RpcParameter import RpcParameter
from VistaRpc import VistaRpc

class VistaSelect(object):

    def __init__(self):
        self._fields = '@'
        self._flags = 'IP'
        self._index = '#'

    @property
    def iens(self):
        return self._iens

    @iens.setter
    def iens(self, value):
        if value[0] != ',': value = ',' + value
        if value[-1] != ',': value += ','
        parts = value[1:-1].split(',', -1)
        for part in parts:
            if not part.isdigit():
                raise VistaException('Invalid IENS')
        self._iens = value

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        if len(value):
            self._fields = value if value.find('@') != -1 else '@;' + value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        if value is None or value == '': value = 'IP'
        if value.find('P') == -1:
            raise VistaException('Current version does packed queries only')
        self._flags = value

    def find(self, cxn):
        self.__prepare()
        self.response = cxn.execute(self.rpc)
        self.__load(self.response)
        return self.records

    def __prepare(self):
        self.__prepare_param_list()
        params = RpcParameter(RpcParameter.LIST, self.param_list)
        self.rpc = VistaRpc.prepare('DDR LISTER', [params])

    def __prepare_param_list(self):
        if not getattr(self, 'file', None):
            raise VistaException('VistaSelect must specify a file')
        self.param_list = [('"FILE"', self.file)]

        if getattr(self, 'iens', None):
            self.param_list += [('"IENS"', self.iens)]

        self.param_list += [('"FIELDS"', getattr(self, 'fields', '@'))]

        self.param_list += [('"FLAGS"', getattr(self, 'flags', 'IP'))]

        if getattr(self, 'number', None):
            self.param_list += [('"MAX"', str(self.number))]

        if getattr(self, 'frum', None):
            self.param_list += [('"FROM"', VistaUtils.adjust_for_search(self.frum))]

        if getattr(self, 'part', None):
            self.param_list += [('"PART"', self.part)]

        self.param_list += [('"XREF"', getattr(self, 'index', '#'))]

        if getattr(self, 'screen', None):
            self.param_list += [('"SCREEN"', self.screen)]

        if getattr(self, 'identifier', None):
            self.param_list += [('"ID"', self.identifier)]

        return self.param_list

    def __load(self, response):
        lines = response.split("\r\n")
        numlines = len(lines)

        # Find starting line...
        linenum = 0
        while linenum < numlines and lines[linenum] != '[BEGIN_diDATA]':
            linenum += 1
        if linenum == numlines:
            raise VistaException('Empty response')
        linenum += 1

        self.records = []
        while linenum < numlines and lines[linenum] != '[END_diDATA]':
            self.records.append(lines[linenum].split('^'))
            linenum += 1
        return self.records




