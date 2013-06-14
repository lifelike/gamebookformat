#!/usr/bin/env python2.7

import StringIO
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
        of = output.OutputFormat(FakeTemplates({}), str)

    def test_write_empty_begin(self):
        of = output.OutputFormat(FakeTemplates({'begin' : 'b %(max)d'}), str)
        out = StringIO.StringIO()
        of.write_begin({'max' : 2}, out)
        self.assertEqual(out.getvalue(), 'b 2')

class TestReferenceFormatter(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        rf = output.ReferenceFormatter(1, {}, "", str)

    def test_get_item(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2}, "%(nr)d", int)
        self.assertEqual(rf['nr'], 1)

    def test_get_quoted_item(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2}, "%(nr)d", str)
        self.assertEqual(rf['nr'], '1')

    def test_get_reference(self):
        rf = output.ReferenceFormatter(1, {'a' : 1, 'b' : 2},
                                       "%(from_nr)d to %(nr)d", None)
        self.assertEqual(rf['b'], '1 to 2')
        self.assertEquals(rf.found, set(['1 to 2']))

if __name__ == '__main__':
    unittest.main()
