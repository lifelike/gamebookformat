from paragraphs import paragraph_refs_format

def default_paragraph_link_render(paragraph, shuffled_paragraphs):
    return str(shuffled_paragraphs.to_nr[paragraph])

class OutputFormat (object):
    def __init__(self, extension, name):
        self.extension = extension
        self.name = name

    def __str__(self):
        return ".%s: %s" % (self.extension, self.name)

    def write(self, book, output):
        self.write_begin(book, output)
        self.write_shuffled_paragraphs(book.shuffle(), output)
        self.write_end(book, output)

    def write_begin(self, book, output):
        pass

    def write_shuffled_paragraphs(self, shuffled_paragraphs, output):
        for p in shuffled_paragraphs.as_list[1:]:
            self.write_paragraph(p, shuffled_paragraphs, output)

    def write_paragraph(self, paragraph, shuffled_paragraphs, output):
        print >> output, shuffled_paragraphs.to_nr[paragraph]
        print >> output, paragraph.format(shuffled_paragraphs,
                                          default_paragraph_link_render)

    def write_end(self, book, output):
        pass

    def supports(self, filename):
        return filename.endswith('.' + self.extension)
