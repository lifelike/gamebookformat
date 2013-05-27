from output import OutputFormat

class DebugFormat (OutputFormat):
    def __init__(self):
        super(DebugFormat, self).__init__('debug', 'Gamebook Debug Output')

    def write_begin(self, book, output):
        print >> output, "BEGIN DEBUG OUTPUT"
        print >> output, "Number of paragraphs: ", book.max

    def write_end(self, book, output):
        print >> output, "END DEBUG OUTPUT"
