import random
import sys

class Paragraph:
    def __init__(self, name, text):
        self.name = name
        self.text = text

    def __repr__(self):
        return "Paragraph(%s, %s)" % (repr(self.name), repr(self.text))

    def format(self, references):
        return self.text % references

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
