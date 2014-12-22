#!/usr/bin/env python2.7

import unittest
from unittest import TestCase

import output

class FakeTemplates(object):
    def __init__(self, d):
        self.d = d

    def get(self, name):
        if name in self.d:
            return self.d[name]
        else:
            return ''

class TestOutputFormat(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        of = output.OutputFormat(FakeTemplates({}), "TEST", False, str)

    def test_format_begin(self):
        of = output.OutputFormat(FakeTemplates({'begin' : 'b %(max)d'}), "TEST", False, str)
        self.assertEqual(of.format_begin({'max' : 2}), 'b 2')

class TestReferenceFormatter(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        rf = output.ReferenceFormatter(1, {}, None, "", "", str)

    def test_get_item(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2}, None,
                                       "%(nr)d", "", int)
        self.assertEqual(rf['nr'], 1)

    def test_get_quoted_item(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2}, None,
                                       "%(nr)d", "", str)
        self.assertEqual(rf['nr'], '1')

    def test_get_reference(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2}, None,
                                       "%(from_nr)d to %(nr)d", "", str)
        self.assertEqual(rf['b'], '1 to 2')

    def test_get_named_reference(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2}, None,
                                       "%(from_nr)d to %(nr)d",
                                       "%(from_nr)d to %(name)s(%(nr)d)", str)
        self.assertEqual(rf.ref('b', 'name'), '1 to name(2)')


if __name__ == '__main__':
    unittest.main()
