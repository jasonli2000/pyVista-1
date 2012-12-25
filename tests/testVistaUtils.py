__author__ = 'Joe'

import unittest
from VistaUtils import VistaUtils

class TestVistaUtils(unittest.TestCase):

    def test_str_pack(self):
        expected = "0000000015something!5here"
        actual = VistaUtils.str_pack("something!5here", 10)
        self.assertEqual(expected, actual)

    def test_prepend_count(self):
        expected = "\x0aSomeString"
        actual = VistaUtils.prepend_count("SomeString")
        self.assertEqual(expected, actual)

        expected = "\x0aDDR LISTER"
        actual = VistaUtils.prepend_count("DDR LISTER")
        self.assertEqual(expected, actual)

    def test_adjust_for_numeric_search(self):
        expected = "244"
        actual = VistaUtils._VistaUtils__adjust_for_numeric_search("245")
        self.assertEqual(expected, actual)

    def test_adjust_for_string_search(self):
        expected = "Snurc~"
        actual = VistaUtils._VistaUtils__adjust_for_string_search("Snurd")
        self.assertEqual(expected, actual)

    def test_adjust_for_search(self):
        expected = "244"
        actual = VistaUtils.adjust_for_search("245")
        self.assertEqual(expected, actual)

        expected = "Snurc~"
        actual = VistaUtils.adjust_for_search("Snurd")
        self.assertEqual(expected, actual)
