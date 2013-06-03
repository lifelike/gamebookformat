#!/usr/bin/env python2.5

import unittest
from unittest import TestCase

import sections

class TestSection(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        p = sections.Section("foo")
        self.assertEqual(p.name, "foo")

class TestBook(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        g = sections.Book()
        self.assertEqual(g.sections, [])
        self.assertEqual(g.nr_sections, {})
        self.assertEqual(g.max, 0)

    def test_old_big_mess(self):
        """This was tested using print statements in the old
        sections __main__. Not pretty. Keeping it here anyway
        as long as it doesn't cause too many problems to update."""
        from sections import section_refs_format
        g = sections.Book()
        c = sections.Section("c", "aaac")
        g.add(sections.Section("a", "aaa"))
        g.add(sections.Section("b", "aaab"))
        g.add(c)
        g.add(sections.Section("d", "aaad"), 22)
        g.add(sections.Section("e", "aaae"), 1)
        g.add(sections.Section("f", "aaaf", 
                                   [sections.SectionItem("fff")]))
        g.add(sections.Section("g", "aaag",
                                   [sections.SectionItem("ggg", "G")]))
        m = sections.Section("m")
        m.addtext("m")
        m.addtext("t")
        g.add(m)
        shuffled = g.shuffle()

        self.assertEqual(len(shuffled.as_list), 23)
        self.assertEqual(section_refs_format('abc', []), 'abc')
        self.assertEqual(section_refs_format('abc%%z', []), 'abc%z')
        self.assertEqual(section_refs_format(
                'abc%sx',
                [sections.Section("p1", "111")]),
                         'abcp1x')
        self.assertEqual(section_refs_format(
                'abc%ry', [sections.Section("p2", "222")]),
                         "abc'p2'y")
        self.assertEqual(section_refs_format('%%a%nbc%su', ["f", c],
                                               shuffled),
                         '%%a%dbccu' % shuffled.name_to_nr["f"])
        self.assertEqual(section_refs_format('abc%nu', ["c"], shuffled),
                         'abc%du' % shuffled.name_to_nr["c"])
        self.assertEqual(section_refs_format('%s', [m]),
                         'm')
        self.assertEqual(m.text, 'mt')

    def test_name_replace(self):
        game = sections.Book()
        game.add(sections.Section('foo'))
        shuffled = game.shuffle()
        self.assertEqual(
            'a1b',
            sections.section_refs_format('a%(foo)nb', [], shuffled))

if __name__ == '__main__':
    unittest.main()
