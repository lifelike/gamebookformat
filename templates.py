import os
import os.path
import sys

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
        raise Exception("Found no template " + name + " for "
                        + self.extension + ".")

    def has_template_in(self, templatedir, name):
        # FIXME better test
        return os.path.exists(self.get_template_filename(templatedir, name))

    def get_in(self, templatedir, name):
        filename = self.get_template_filename(templatedir, name)
        f = open(filename, "r")
        template = f.read()
        f.close()
        self.cached_templates[name] = template
        return template

    def get_template_filename(self, templatedir, name):
        return os.path.join(templatedir,
                            self.extension,
                            name + "." + self.extension)

