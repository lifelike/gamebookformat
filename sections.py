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

class ShuffledSection (Section):
    def __init__(self, nr, section):
        self.nr = nr
        self.name = section.name
        self.text = section.text
        self.tags = section.tags.copy()

    def __repr__(self):
        return "ShuffledSection(%d, %s, %s, %s)" % (self.nr,
                                                    repr(self.name),
                                                    repr(self.text),
                                                    repr(self.tags))

class IntroSection (Section):
    def __init__(self, section):
        self.nr = -1
        self.name = section.name
        self.text = section.text
        self.tags = section.tags.copy()

    def __repr__(self):
        return "IntroSection(%d, %s, %s, %s)" % (repr(self.name),
                                                 repr(self.text),
                                                 repr(self.tags))

class ShuffledSections:
    def __init__(self, as_list, from_nr, from_name, nr_sections, missingto):
        self.as_list = as_list
        self.from_nr = from_nr
        self.from_name = from_name
        self.name_to_nr = {}
        for n in from_name:
            self.name_to_nr[n] = from_name[n].nr
        for nr in nr_sections:
            self.name_to_nr[nr_sections[nr]] = nr
        self.missingto = missingto

STR_BOOK_CONFIG = set(['id', 'title', 'author', 'starttext', 'hideintrotext',
                       'showintrotext', 'resumetext', 'missingto'])
INT_BOOK_CONFIG = set(['max'])

class Book:
    def __init__(self, bookid='gamebook', includetag=None):
        self.sections = []
        self.introsections = []
        self.from_name = {}
        self.nr_sections = {}
        self.codewords = set()
        self.includetag = includetag
        self.config = {'max' : 0,
                       'title' : 'Gamebook',
                       'author' : '',
                       'starttext' : 'Turn to 1 to begin.',
                       'hideintrotext' : '(hide instructions)',
                       'showintrotext' : '(show instructions)',
                       'resumetext' : 'Resume saved game.',
                       'missingto' : None,
                       'id' : bookid}

    def configure(self, name, value):
        if name in INT_BOOK_CONFIG:
            self.config[name] = int(value)
        elif name in STR_BOOK_CONFIG:
            self.config[name] = value
        else:
            raise Exception("Unknown book option '%s'." % name)

    def add(self, section):
        if self.includetag and not section.hastag(self.includetag):
            return
        if section.name in self.from_name:
            raise Exception('Duplicate section names (%s) not allowed.' %
                            section.name)
        self.sections.append(section)
        self.from_name[section.name] = section
        if len(self.sections) > self.config['max']:
            self.config['max'] = len(self.sections)

    def addintro(self, section):
        self.introsections.append(IntroSection(section))

    def add_codeword(self, word):
        self.codewords.add(word)

    def force_section_nr(self, name, nr):
        self.nr_sections[nr] = name
        if nr > self.config['max']:
            self.config['max'] = nr

    def shuffle(self, reallyshuffle=True):
        as_list = [None]
        from_nr = {}
        shuffled = self.sections[:]
        shuffled_from_name = {}
        while len(shuffled) < self.config['max']:
            dummy = Section('Dummy', '')
            dummy.add_tags(['dummy'])
            shuffled.append(dummy)
        for p in self.nr_sections.values():
            if p in self.from_name:
                shuffled.remove(self.from_name[p])
        if reallyshuffle:
            random.shuffle(shuffled)
        for nr in range(1, self.config['max'] + 1):
            if (self.nr_sections.has_key(nr)
                and self.nr_sections[nr] in self.from_name):
                section = ShuffledSection(nr, self.from_name[
                    self.nr_sections[nr]])
            elif len(shuffled):
                section = ShuffledSection(nr, shuffled.pop())
            else:
                section = None
            as_list.append(section)
            from_nr[nr] = section
            if section:
                shuffled_from_name[section.name] = section
        return ShuffledSections(as_list, from_nr, shuffled_from_name,
                                self.nr_sections,
                                self.config['missingto'])
