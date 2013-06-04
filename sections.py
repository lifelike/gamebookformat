import random
import sys

class Section:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.tags = set()

    def add_tags(self, tags):
        self.tags.update(set(tags))

    def hastag(self, tag):
        return tag in self.tags

    def __repr__(self):
        return "Section(%s, %s, %s)" % (repr(self.name), repr(self.text),
                                        repr(self.tags))

    def format(self, references):
        i = 0
        res = ""
        while i < len(self.text):
            ref_start = self.text.find('[[', i)
            tag_start = self.text.find('[', i)
            if ref_start >= 0 and ref_start <= tag_start:
                res += self.text[i:ref_start]
                ref_end = self.text.find(']]', ref_start)
                if ref_end > ref_start:
                    ref = self.text[ref_start+2:ref_end]
                    res += references[ref]
                    i = ref_end + 2
                else:
                    raise Exception('Mismatched ref start [[ in section %s' %
                                    self.name)
            elif tag_start >= 0:
                res += self.text[i:tag_start]
                tag_end = self.text.find(']', tag_start)
                if tag_end < 0:
                    raise Exception('Mismatched tag start [ in section %s' %
                                    self.name)
                tag = self.text[tag_start+1:tag_end]
                end_tag_start = self.text.find('[', tag_end)
                if (not end_tag_start > tag_end
                    and self.text[end_tag_start].startswith('[/' + tag + ']')):
                    raise Exception('Bad format %s tag in %s.' % (
                        tag, self.name))
                tagtext = self.text[tag_end+1:end_tag_start]
                print tag, tagtext
                #FIXME actually handle tags
                res += tagtext
                i = self.text.find(']', end_tag_start) + 1
            else:
                res += self.text[i:]
                break
        return res

class ShuffledSections:
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
        self.sections = []
        self.from_name = {}
        self.nr_sections = {}
        self.max = 0
        self.codewords = set()

    def add(self, section):
        if section.name in self.from_name:
            raise Exception('Duplicate section names (%s) not allowed.' %
                            section.name)
        self.sections.append(section)
        self.from_name[section.name] = section
        if len(self.sections) > self.max:
            self.max = len(self.sections)

    def add_codeword(self, word):
        self.codewords.add(word)

    def force_section_nr(self, name, nr):
        self.nr_sections[nr] = name
        if nr > self.max:
            self.max = nr

    def shuffle(self):
        as_list = [None]
        from_nr = {}
        to_nr = {}
        shuffled = self.sections[:]
        for p in self.nr_sections.values():
            shuffled.remove(self.from_name[p])
        random.shuffle(shuffled)
        for nr in range(1, self.max + 1):
            if self.nr_sections.has_key(nr):
                section = self.from_name[self.nr_sections[nr]]
            elif len(shuffled):
                section = shuffled.pop()
            else:
                section = None
            as_list.append(section)
            from_nr[nr] = section
            if section:
                to_nr[section] = nr
        return ShuffledSections(as_list, from_nr, to_nr, self.from_name.copy())

class Item (object):
    def __init__(self, name):
        self.name = name

class Hero (object):
    "The hero (player character) of a Book."
    def __init__(self):
        self.carrying_capacity = 10
        self.skills = set()
