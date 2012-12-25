__author__ = 'Joe'

class VistaUtils(object):

    @staticmethod
    def str_pack(s, width):
        slth = str(len(s))
        return slth.rjust(width, '0') + s

    @staticmethod
    def prepend_count(s):
        return chr(len(s)) + s

    @staticmethod
    def __adjust_for_numeric_search(s):
        return str(int(s) - 1)

    @staticmethod
    def __adjust_for_string_search(s):
        return s[0:-1] + chr(ord(s[-1])-1) + '~'

    @staticmethod
    def adjust_for_search(s):
        if s.isdigit():
            return VistaUtils.__adjust_for_numeric_search(s)
        else:
            return VistaUtils.__adjust_for_string_search(s)

