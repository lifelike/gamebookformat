import os
import os.path
import sys

class Templates (object):
    def __init__(self, extension):
        self.extension = extension
        self.templates_dir = os.path.join(os.path.dirname(sys.argv[0]),
                                          "templates",
                                          extension)
        self.cached_templates = {}

    def get(self, name):
        if name in self.cached_templates:
            return self.cached_templates[name]
        filename = os.path.join(self.templates_dir,
                                name + "." + self.extension)
        f = open(filename, "r")
        template = f.read()
        f.close()
        self.cached_templates[name] = template
        return template

