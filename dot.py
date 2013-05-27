from output import OutputFormat

class DotParagraphFormat (object):
    def __init__(self, fromparagraph):
        self.fromparagraph = fromparagraph
        self.toparagraphs = []

    def __call__(self, toparagraph, shuffled_paragraphs):
        self.toparagraphs.append(toparagraph)
        return ''

    def write(self, shuffled_paragraphs, output):
        for toparagraph in self.toparagraphs:
            print >> output, "%s->%s" % (
                shuffled_paragraphs.to_nr[self.fromparagraph],
                shuffled_paragraphs.to_nr[toparagraph])

class DotFormat (OutputFormat):
    def __init__(self):
        super(DotFormat, self).__init__('dot', 'Graphviz paragraph flowchart')

    def write_begin(self, book, output):
        print >> output, "digraph gamebook {"

    def write_paragraph(self, paragraph, shuffled_paragraphs, output):
        paragraphformat = DotParagraphFormat(paragraph)
        paragraph.format(shuffled_paragraphs, paragraphformat)
        paragraphformat.write(shuffled_paragraphs, output)

    def write_end(self, book, output):
        print >> output, "}"


