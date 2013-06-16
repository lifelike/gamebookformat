#!/usr/bin/env python2.7

import unittest
from unittest import TestCase

import sections

class TestSection(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        sec = sections.Section("nnn", "text")
        self.assertEqual(sec.name, "nnn")
        self.assertEqual(sec.text, "text")

    def test_add_tags(self):
        sec = sections.Section("nnn", "text")
        sec.add_tags(['a', 'b'])
        self.assertTrue(sec.hastag('a'))
        self.assertTrue(sec.hastag('b'))
        sec.add_tags(['c', 'd'])
        self.assertTrue(sec.hastag('a'))
        self.assertTrue(sec.hastag('b'))
        self.assertTrue(sec.hastag('c'))
        self.assertTrue(sec.hastag('d'))

class TestBook(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        b = sections.Book()
        self.assertEqual(b.sections, [])
        self.assertEqual(b.nr_sections, {})
        self.assertEqual(b.config['max'], 0)

    def test_includetag(self):
        b = sections.Book(includetag='test')
        sec = sections.Section("nnn", "text")
        sec.add_tags(['some', 'test', 'other'])
        b.add(sec)
        self.assertEqual(b.sections, [sec])

    def test_excludetag(self):
        b = sections.Book(includetag='test')
        sec = sections.Section("nnn", "text")
        sec.add_tags(['some', 'other'])
        b.add(sec)
        self.assertEqual(b.sections, [])

if __name__ == '__main__':
    unittest.main()
