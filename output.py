import os
import os.path
import sys

class OutputFormat (object):
    "Handles book output. Big FIXME required to make sense."
    def __init__(self, templates, quote):
        self.templates = templates
        self.quote = quote

    def write_begin(self, book, output):
        # FIXME make sure book config is properly quoted
        print >> output, self.format_with_template("begin", book.config)

    def write_intro_sections(self, book, shuffled_sections, output):
        for s in book.introsections:
            if not s.hastag('dummy'):
                self.write_intro_section(s, shuffled_sections, output)

    def write_intro_section(self, section, shuffled_sections, output):
        # FIXME some serious code-duplication here
        refs = []
        refsdict = ReferenceFormatter(section, shuffled_sections,
                                      self.format_with_template("section_ref"),
                                      self.quote)
        formatted_text = self.format_section(section, refsdict)
        print >> output, self.format_with_template("introsection", {
            'name' : section.name,
            'text' : formatted_text,
            'refs' : '\n'.join(refsdict.getfound()) # hack for DOT output
        }),

    def write_sections_begin(self, book, output):
        print >> output, self.format_with_template("sections_begin", book.config);

    def write_shuffled_sections(self, shuffled_sections, output):
        for i, p in enumerate(shuffled_sections.as_list):
            if p and not p.hastag('dummy'):
                self.write_section(p, shuffled_sections, output)
            elif i > 0:
                self.write_empty_section(i, output)

    def write_section(self, section, shuffled_sections, output):
        refs = []
        refsdict = ReferenceFormatter(section, shuffled_sections,
                                      self.format_with_template("section_ref"),
                                      self.quote)
        formatted_text = self.format_section(section, refsdict)
        print >> output, self.format_with_template("section", {
            'nr' : section.nr,
            'name' : section.name,
            'text' : formatted_text,
            'refs' : '\n'.join(refsdict.getfound()) # hack for DOT output
        }),

    def format_section(self, section, references):
        i = 0
        res = ""
        # FIXME refactor for readability once good tests are in place
        while i < len(section.text):
            ref_start = section.text.find('[[', i)
            tag_start = section.text.find('[', i)
            if ref_start >= 0 and ref_start <= tag_start:
                res += self.quote(section.text[i:ref_start])
                ref_end = section.text.find(']]', ref_start)
                if ref_end > ref_start:
                    ref = section.text[ref_start+2:ref_end]
                    splitref = ref.split()
                    if len(splitref) > 1:
                        for refmod in splitref[:-1]:
                            res += self.format_with_template(refmod,
                                                             references)
                    res += references[splitref[-1]]
                    i = ref_end + 2
                else:
                    raise Exception('Mismatched ref start [[ in section %s' %
                                    self.name)
            elif tag_start >= 0:
                res += self.quote(section.text[i:tag_start])
                tag_end = section.text.find(']', tag_start)
                if tag_end < 0:
                    raise Exception('Mismatched tag start [ in section %s' %
                                    self.name)
                tag = section.text[tag_start+1:tag_end].strip()
                tagparts = tag.split()
                tagname = tagparts[0]
                end_tag_start = section.text.find('[', tag_end)
                if (not end_tag_start > tag_end
                    and section.text[end_tag_start].startswith('[/' + tagname
                                                               + ']')):
                    raise Exception('Bad format %s tag in %s.' % (
                        tag, self.name))
                inner = section.text[tag_end+1:end_tag_start]
                # FIXME this pollutes the mutable references object
                references['inner'] = self.quote(self.quote(inner))
                for i, arg in enumerate(tagparts[1:]):
                    references['arg%d' % (i+1)] = self.quote(arg)
                f = self.format_with_template(tagname,
                                              references)
                if len(f) > 0:
                    res += f
                else:
                    res += self.quote(inner)
                i = section.text.find(']', end_tag_start) + 1
            else:
                res += self.quote(section.text[i:])
                break
        return res

    def write_empty_section(self, nr, output):
        print >> output, self.format_with_template("empty_section", {
            'nr' : nr,
        }),

    def write_end(self, book, output):
        print >> output, self.format_with_template("end", book.config),

    def format_with_template(self, name, values=None):
        template = self.templates.get(name)
        if values:
            return template % values
        else:
            return template

class ReferenceFormatter (object):
    "There is probably a better way, but this hack seems to work."
    def __init__(self, section, shuffled_sections, ref_template, quote):
        self.section = section
        self.shuffled_sections = shuffled_sections
        self.found = set()
        self.ref_template = ref_template
        self.items = {'nr' : section.nr}
        self.quote = quote

    def __getitem__(self, key):
        if key in self.items:
            return self.quote(self.items[key])
        to_section = self.shuffled_sections.from_name[key]
        res = self.ref_template % {
            'nr' : to_section.nr,
            'from_nr' : self.section.nr
        }
        if key in self.shuffled_sections.name_to_nr:
            self.found.add(res)
        return res

    def getfound(self):
        return list(self.found)

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]
