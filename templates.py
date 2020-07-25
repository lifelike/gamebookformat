#!/usr/bin/env python2

import re
import os
import os.path
import sys

PREPROCESS_RE = re.compile("^\s*#")
INCLUDE_RE = re.compile('^\s*#include\s*"([-\w]+)"')

class Templates (object):
    def __init__(self, templatedirs, extension):
        self.extension = extension
        self.cached_templates = {}
        self.templatedirs = templatedirs

    def get(self, name):
        if name in self.cached_templates:
            return self.cached_templates[name]
        for templatedir in self.templatedirs:
            if self.has_template_in(templatedir, name):
                return self.get_in(templatedir, name)
            elif self.has_template_in(templatedir, name, 'DEFAULT', 'txt'):
                return self.get_in(templatedir, name, 'DEFAULT', 'txt')
        return ""

    def has_template_in(self, templatedir, name, subdir=None, extension=None):
        # FIXME better test
        return os.path.exists(self.get_template_filename(templatedir, name,
                                                         subdir,
                                                         extension))

    def get_in(self, templatedir, name, subdir=None, extension=None):
        filename = self.get_template_filename(templatedir, name, subdir, extension)
        f = open(filename, "r")
        template = self.read_template(f);
        f.close()
        self.cached_templates[name] = template
        return template

    def read_template(self, f):
        res = ""
        for line in f.readlines():
            if PREPROCESS_RE.match(line):
                res += self.preprocessline(line)
            else:
                res += line
        return res

    def preprocessline(self, line):
        m = INCLUDE_RE.match(line)
        if m:
            return self.get(m.group(1))
        else:
            return line

    def get_template_filename(self, templatedir, name, subdir=None, extension=None):
        if not subdir:
            subdir = self.extension
        if not extension:
            extension = self.extension
        return os.path.join(templatedir, subdir, name + "." + extension)

if __name__ == '__main__':
    templates = Templates(['templates'], sys.argv[1])
    print templates.get(sys.argv[2])
