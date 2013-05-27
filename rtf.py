from output import OutputFormat

class RtfFormat (OutputFormat):
    def __init__(self):
        super(RtfFormat, self).__init__('rtf', 'Rich Text Format')

    def write(self, book, output):
        raise Exception("RTF output format not yet supported. :(")
