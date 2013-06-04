import os
import os.path
import sys

class OutputFormat (object):
    "Handles book output. Big FIXME required to make sense."
    def __init__(self, templates):
        self.templates = templates

    def write_begin(self, book, output):
        print >> output, self.format_with_template("begin", {
            'max' : book.max
        }),

    def write_shuffled_sections(self, shuffled_sections, output):
        for i, p in enumerate(shuffled_sections.as_list):
            if p:
                self.write_section(p, shuffled_sections, output)
            elif i > 0:
                self.write_empty_section(i, output)

    def write_section(self, section, shuffled_sections, output):
        refs = []
        refsdict = ReferenceFormatter(section, shuffled_sections,
                                      self.format_with_template("section_ref"))
        formatted_text = section.format(refsdict)
        print >> output, self.format_with_template("section", {
            'nr' : shuffled_sections.to_nr[section],
            'name' : section.name,
            'text' : formatted_text,
            'refs' : '\n'.join(refsdict.getfound()) # hack for DOT output
        }),

    def write_empty_section(self, nr, output):
        print >> output, self.format_with_template("empty_section", {
            'nr' : nr,
        }),

    def write_end(self, book, output):
        print >> output, self.format_with_template("end"),

    def format_with_template(self, name, values=None):
        template = self.templates.get(name)
        if values:
            return template % values
        else:
            return template

class ReferenceFormatter (object):
    "There is probably a better way, but this hack seems to work."
    def __init__(self, section, shuffled_sections, ref_template):
        self.section = section
        self.shuffled_sections = shuffled_sections
        self.found = set()
        self.ref_template = ref_template

    def __getitem__(self, key):
        to_section = self.shuffled_sections.from_name[key]
        res = self.ref_template % {
            'nr' : self.shuffled_sections.to_nr[to_section],
            'from_nr' : self.shuffled_sections.to_nr[self.section]
        }
        if key in self.shuffled_sections.name_to_nr:
            self.found.add(res)
        return res

    def getfound(self):
        return list(self.found)
