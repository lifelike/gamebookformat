#!/usr/bin/env python2.5

import random
import sys

def paragraph_refs_format(s,
                          refs,
                          shuffled=None,
                          render_callback=None,
                          bad_callback=None):
    """
render_callback, if set, must be a function accepting a paragraph name
and a ShuffledParagraphs object. It must return a string formatting
of a link to that reference. Its use is for instance if you render
the paragraphs to HTML you can return a HTML link. It will only be
used if format %c is used.

bad_callback, if set, must be a function accepting a paragraph
name and a ShuffledParagraphs object. It may attempt to construct
a new Paragraph object standing in for a missing paragraph, if there
is a way to automatically construct some paragraphs in the game.
If it can not construct  a paragraph it should return None or False
which will cause the formatting to fail and raise an exception.
"""
    oi = 0
    next_ref = 0
    res = ''
    i = s.find('%')
    while i >= 0:
        res = res + s[oi:i]
        skip = 0
        code = s[i+1]
        if code == '%':
            res += '%'
        else:
            if code == '(':
                ei = s.find(')', i+1)
                if ei < 0:
                    raise "bad format, missing ) after %("
                ref = s[i+2:ei]
                skip = len(ref) + 2
                code = s[ei+1]
            else:
                ref = refs[next_ref]
            if type(ref) in set([str, unicode]):
                if ref in shuffled.from_name:
                    ref = shuffled.from_name[ref]
                elif bad_callback:
                    created_ref = bad_callback(ref, shuffled)
                    if not created_ref:
                        raise "bad reference " + ref
                    ref = created_ref
            if code == 'n':
                res += str(shuffled.to_nr[ref])
            elif code == 'c':
                if render_callback:
                    res += render_callback(ref, shuffled)
                else:
                    res += str(ref)
            elif code == 's':
                res += str(ref.name)
            elif code == 'r':
                res += repr(ref.name)
            next_ref = next_ref + 1
        oi = i + 2 + skip
        i = s.find('%', oi)
    return res + s[oi:]

class ParagraphItem:
    def __init__(self, text, refs=None, title=None):
        self.text = text
        self.title = title
        if refs:
            self.refs = refs
        else:
            self.refs = []

    def __repr__(self):
        return "ParagraphItem(%s, %s, %s)" % (self.text.__repr__(),
                                          self.refs.__repr__(),
                                          self.title.__repr__())

    def format(self, shuffled=None, render_callback=None, bad_callback=None):
        return paragraph_refs_format(self.text, self.refs, shuffled, render_callback,
                                     bad_callback)

class Paragraph:
    def __init__(self, name, text=None, refs=None, items=None):
        self.name = name
        if text:
            self.text = text
        else:
            self.text = ''
        if items:
            self.items = items
        else:
            self.items = []
        if refs:
            self.refs = refs
        else:
            self.refs = []

    def __repr__(self):
        return "Paragraph(%s, %s, %s, %s)" % (self.name.__repr__(),
                                              self.text.__repr__(),
                                              self.refs.__repr__(),
                                              self.items.__repr__())
    def addtext(self, moretext):
        self.text = self.text + moretext

    def format(self, shuffled=None, render_callback=None, bad_callback=None):
        return paragraph_refs_format(self.text, self.refs, shuffled, render_callback,
                                     bad_callback)

class ShuffledParagraphs:
    def __init__(self, as_list, from_nr, to_nr, from_name):
        self.as_list = as_list
        self.from_nr = from_nr
        self.to_nr = to_nr
        self.from_name = from_name
        self.name_to_nr = {}
        for n in from_name:
            self.name_to_nr[n] = to_nr[from_name[n]]

class Book:
    def __init__(self):
        self.paragraphs = []
        self.nr_paragraphs = {}
        self.max = 0

    def add(self, paragraph, nr=None):
        self.paragraphs.append(paragraph)
        if len(self.paragraphs) > self.max:
            self.max = len(self.paragraphs)
        if nr:
            self.nr_paragraphs[nr] = paragraph
            if nr > self.max:
                self.max = nr

    def shuffle(self):
        as_list = [None]
        from_nr = {}
        to_nr = {}
        from_name = {}
        shuffled = self.paragraphs[:]
        for p in self.nr_paragraphs.values():
            shuffled.remove(p)
        random.shuffle(shuffled)
        for nr in range(1, self.max + 1):
            if self.nr_paragraphs.has_key(nr):
                paragraph = self.nr_paragraphs[nr]
            elif len(shuffled):
                paragraph = shuffled.pop()
            else:
                paragraph = None
            as_list.append(paragraph)
            from_nr[nr] = paragraph
            if paragraph:
                to_nr[paragraph] = nr
                from_name[paragraph.name] = paragraph
        return ShuffledParagraphs(as_list, from_nr, to_nr, from_name)
