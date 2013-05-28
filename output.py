import os
import os.path
import sys

from paragraphs import paragraph_refs_format

class OutputFormat (object):
    def __init__(self, extension, name):
        self.extension = extension
        self.name = name
        self.cached_templates = {}

    def __str__(self):
        return ".%s: %s" % (self.extension, self.name)

    def write(self, book, output):
        self.write_begin(book, output)
        self.write_shuffled_paragraphs(book.shuffle(), output)
        self.write_end(book, output)

    def write_begin(self, book, output):
        print >> output, self.load_template("begin") % {
            'max' : book.max
        },

    def write_shuffled_paragraphs(self, shuffled_paragraphs, output):
        for p in shuffled_paragraphs.as_list[1:]:
            self.write_paragraph(p, shuffled_paragraphs, output)

    def write_paragraph(self, paragraph, shuffled_paragraphs, output):
        refs = []
        def paragraph_link_render(to_paragraph, shuffled_paragraphs):
            s = self.load_template("paragraph_ref") %  {
                'nr' : shuffled_paragraphs.to_nr[to_paragraph],
                'from_nr' : shuffled_paragraphs.to_nr[paragraph]
            }
            refs.append(s)
            return s
        formatted_text = paragraph.format(shuffled_paragraphs,
                                      paragraph_link_render)
        print >> output, self.load_template("paragraph") % {
            'nr' : shuffled_paragraphs.to_nr[paragraph],
            'text' : formatted_text,
            'refs' : '\n'.join(refs) # hack for DOT output reallyn
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
                                "output_formats",
                                self.extension,
                                name + "." + self.extension)
        f = open(filename, "r")
        template = f.read()
        f.close()
        self.cached_templates[name] = template
        return template

