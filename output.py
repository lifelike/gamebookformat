import os
import os.path
import sys

COUNTER_CREATE_TAG = 'count'
COUNTER_USE_TAGS = set(['set', 'inc', 'dec', 'min',
                        'lessthan', 'morethan', 'atleast'])

class OutputFormat (object):
    "Handles book output. Big FIXME required to make sense."
    def __init__(self, templates, quote, name):
        self.templates = templates
        self.format_quote = quote
        self.name = name
        self.counter_names = {}

    def quote(self, s):
        if s:
            return self.format_quote(s)
        else:
            return ""

    def format_begin(self, bookconfig):
        # FIXME make sure book config is properly quoted
        return self.format_with_template("begin", bookconfig)

    def format_intro_sections(self, introsections, shuffled_sections):
        res = ""
        for s in introsections:
            if not s.hastag('dummy'):
                res += self.format_intro_section(s, shuffled_sections)
        return res

    def format_intro_section(self, section, shuffled_sections):
        # FIXME some serious code-duplication here
        refs = []
        refsdict = ReferenceFormatter(section.nr,
                                      shuffled_sections.name_to_nr,
                                      shuffled_sections.missingto,
                                      self.templates.get("section_ref"),
                                      self.templates.get("named_section_ref"),
                                      self.quote)
        formatted_text = self.format_section_body(section, refsdict)
        return self.format_with_template("introsection", {
            'name' : section.name,
            'text' : formatted_text
        })

    def format_sections_begin(self, bookconfig):
        return self.format_with_template("sections_begin",
                                         bookconfig)

    def format_shuffled_sections(self, shuffled_sections):
        res = ""
        for i, p in enumerate(shuffled_sections.as_list):
            if p and not p.hastag('dummy'):
                res += self.format_section(p, shuffled_sections)
            elif i > 0:
                res += self.format_empty_section(i)
        return res

    def format_section(self, section, shuffled_sections):
        refs = []
        refsdict = ReferenceFormatter(section.nr,
                                      shuffled_sections.name_to_nr,
                                      shuffled_sections.missingto,
                                      self.templates.get("section_ref"),
                                      self.templates.get("named_section_ref"),
                                      self.quote)
        formatted_text = self.format_section_body(section, refsdict)
        return self.format_with_template("section", {
            'nr' : section.nr,
            'name' : section.name,
            'text' : formatted_text
        })

    def format_section_body(self, section, references):
        i = 0
        res = ""
        # FIXME refactor for readability once good tests are in place
        while i < len(section.text):
            ref_start = section.text.find('[[', i)
            tag_start = section.text.find('[', i)
            ref_name = None
            if ref_start >= 0 and ref_start <= tag_start:
                res += self.format_text(section.text[i:ref_start])
                ref_end = section.text.find(']]', ref_start)
                if ref_end > ref_start:
                    ref_name_div_start = section.text.find('][',
                                                       ref_start, ref_end)
                    if ref_name_div_start > ref_start:
                        ref_name = section.text[ref_name_div_start+2:ref_end]
                        ref = section.text[ref_start+2:ref_name_div_start]
                    else:
                        ref = section.text[ref_start+2:ref_end]
                    splitref = ref.split()
                    if len(splitref) > 1:
                        for refmod in splitref[:-1]:
                            res += self.format_with_template(refmod,
                                                             references)
                    res += references.ref(splitref[-1], ref_name)
                    i = ref_end + 2
                else:
                    raise Exception('Mismatched ref start [[ in section %s' %
                                    self.name)
            elif tag_start >= 0:
                res += self.format_text(section.text[i:tag_start])
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
                references['inner'] = self.quote(inner)
                for i, arg in enumerate(tagparts[1:]):
                    references['arg%d' % (i+1)] = self.quote(arg)
                if tagname == COUNTER_CREATE_TAG and len(tagparts) > 1:
                    self.counter_names[tagparts[1]] = self.quote(inner)
                    references['counter'] = self.quote(inner)
                elif tagname in COUNTER_USE_TAGS and len(tagparts) > 1:
                    if tagparts[1] in self.counter_names:
                        references['counter'] = self.counter_names[tagparts[1]]
                f = self.format_with_template(tagname, references)
                if len(f) > 0:
                    res += f
                else:
                    res += self.quote(inner)
                i = section.text.find(']', end_tag_start) + 1
            else:
                res += self.format_text(section.text[i:])
                break
        return res

    def format_text(self, text):
        return self.format_with_template('text', {'text' : self.quote(text)})

    def format_empty_section(self, nr):
        return self.format_with_template("empty_section", {
            'nr' : nr,
        })

    def format_end(self, bookconfig):
        return self.format_with_template("end", bookconfig)

    def format_with_template(self, name, values=None):
        template = self.templates.get(name)
        if values:
            return template % values
        else:
            return template

class ReferenceFormatter (object):
    "There is probably a better way, but this hack seems to work."
    def __init__(self, from_nr, name_to_nr, missingto, ref_template,
                 named_ref_template, quote):
        self.from_nr = from_nr
        self.name_to_nr = name_to_nr
        self.ref_template = ref_template
        self.named_ref_template = named_ref_template
        self.items = {'nr' : from_nr}
        self.quote = quote
        self.missingto = missingto

    def get_to_nr(self, key):
        if key in self.name_to_nr:
            return self.name_to_nr[key]
        elif self.missingto in self.name_to_nr:
            return self.name_to_nr[self.missingto]
        else:
            raise Exception('Missing reference target: %s' % key)

    def __getitem__(self, key):
        if key in self.items:
            return self.quote(self.items[key])
        else:
            return self.ref_template % {
            'nr' : self.get_to_nr(key),
            'from_nr' : self.from_nr
            }

    def ref(self, key, name):
        values = {
            'nr' : self.get_to_nr(key),
            'from_nr' : self.from_nr,
            'name' : self.quote(name)
        }
        if name:
            return self.named_ref_template % values
        else:
            return self.ref_template % values

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]
