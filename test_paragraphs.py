#!/usr/bin/env python2.5

import unittest
from unittest import TestCase

import paragraphs

class TestParagraph(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        p = paragraphs.Paragraph("foo")
        self.assertEqual(p.name, "foo")

class TestBook(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        g = paragraphs.Book()
        self.assertEqual(g.paragraphs, [])
        self.assertEqual(g.nr_paragraphs, {})
        self.assertEqual(g.max, 0)

    def test_old_big_mess(self):
        """This was tested using print statements in the old
        paragraphs __main__. Not pretty. Keeping it here anyway
        as long as it doesn't cause too many problems to update."""
        from paragraphs import paragraph_refs_format
        g = paragraphs.Book()
        c = paragraphs.Paragraph("c", "aaac")
        g.add(paragraphs.Paragraph("a", "aaa"))
        g.add(paragraphs.Paragraph("b", "aaab"))
        g.add(c)
        g.add(paragraphs.Paragraph("d", "aaad"), 22)
        g.add(paragraphs.Paragraph("e", "aaae"), 1)
        g.add(paragraphs.Paragraph("f", "aaaf", 
                                   [paragraphs.ParagraphItem("fff")]))
        g.add(paragraphs.Paragraph("g", "aaag",
                                   [paragraphs.ParagraphItem("ggg", "G")]))
        m = paragraphs.Paragraph("m")
        m.addtext("m")
        m.addtext("t")
        g.add(m)
        shuffled = g.shuffle()

        self.assertEqual(len(shuffled.as_list), 23)
        self.assertEqual(paragraph_refs_format('abc', []), 'abc')
        self.assertEqual(paragraph_refs_format('abc%%z', []), 'abc%z')
        self.assertEqual(paragraph_refs_format(
                'abc%sx',
                [paragraphs.Paragraph("p1", "111")]),
                         'abcp1x')
        self.assertEqual(paragraph_refs_format(
                'abc%ry', [paragraphs.Paragraph("p2", "222")]),
                         "abc'p2'y")
        self.assertEqual(paragraph_refs_format('%%a%nbc%su', ["f", c],
                                               shuffled),
                         '%%a%dbccu' % shuffled.name_to_nr["f"])
        self.assertEqual(paragraph_refs_format('abc%nu', ["c"], shuffled),
                         'abc%du' % shuffled.name_to_nr["c"])
        self.assertEqual(paragraph_refs_format('%s', [m]),
                         'm')
        self.assertEqual(m.text, 'mt')

    def test_name_replace(self):
        game = paragraphs.Book()
        game.add(paragraphs.Paragraph('foo'))
        shuffled = game.shuffle()
        self.assertEqual(
            'a1b',
            paragraphs.paragraph_refs_format('a%(foo)nb', [], shuffled))

if __name__ == '__main__':
    unittest.main()
