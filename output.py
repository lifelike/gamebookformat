import os
import os.path
import sys

class OutputFormat (object):
    def __init__(self, extension, name):
        self.extension = extension
        self.name = name
        self.cached_templates = {}

    def __str__(self):
        return ".%s: %s" % (self.extension, self.name)

    def write(self, book, output):
        self.write_begin(book, output)
        self.write_shuffled_sections(book.shuffle(), output)
        self.write_end(book, output)

    def write_begin(self, book, output):
        print >> output, self.load_template("begin") % {
            'max' : book.max
        },

    def write_shuffled_sections(self, shuffled_sections, output):
        for p in shuffled_sections.as_list[1:]:
            self.write_section(p, shuffled_sections, output)

    def write_section(self, section, shuffled_sections, output):
        refs = []
        refsdict = ReferenceFormatter(section, shuffled_sections,
                                      self.load_template("section_ref"))
        formatted_text = section.format(refsdict)
        print >> output, self.load_template("section") % {
            'nr' : shuffled_sections.to_nr[section],
            'text' : formatted_text,
            'refs' : '\n'.join(refsdict.getfound()) # hack for DOT output
        },

    def write_end(self, book, output):
        print >> output, self.load_template("end") % {},

    def supports(self, filename):
        return filename.endswith('.' + self.extension)

    def load_template(self, name):
        "Templates is a mess and do not belong in the output class really."
        if name in self.cached_templates:
            return self.cached_templates[name]
        filename = os.path.join(os.path.dirname(sys.argv[0]),
                                "templates",
                                self.extension,
                                name + "." + self.extension)
        f = open(filename, "r")
        template = f.read()
        f.close()
        self.cached_templates[name] = template
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
