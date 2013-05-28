from output import OutputFormat

def format_rtf_paragraph_ref(paragraph, shuffled_paragraphs):
    return ("\\b %d\n\\b0" % shuffled_paragraphs.to_nr[paragraph])

class RtfFormat (OutputFormat):
    def __init__(self):
        super(RtfFormat, self).__init__('rtf', 'Rich Text Format')

    def write_begin(self, book, output):
        print >> output, """
{\\rtf1\\ansi\\ansicpg1252\\cocoartf1038\\cocoasubrtf360
{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;}
{\\colortbl;\\red255\\green255\\blue255;}
\\paperw11900\\paperh16840\\margl1440\\margr1440\\vieww14140\\viewh14860\\viewkind0
\\pard\\tx566\\tx1133\\tx1700\\tx2267\\tx2834\\tx3401\\tx3968\\tx4535\\tx5102\\tx5669\\tx6236\\tx6803\\ql\\qnatural\\pardirnatural

\\f0\\b\\fs24 \\cf0""",

    def write_shuffled_paragraphs(self, shuffled_paragraphs, output):
        for p in shuffled_paragraphs.as_list[1:]:
            self.write_paragraph(p, shuffled_paragraphs, output)

    def write_paragraph(self, paragraph, shuffled_paragraphs, output):
        print >> output, format_rtf_paragraph_ref(paragraph,
                                                    shuffled_paragraphs)
        print >> output, " - "
        print >> output, paragraph.format(shuffled_paragraphs,
                                          format_rtf_paragraph_ref)
        print >> output, "\\\n\\"

    def write_end(self, book, output):
        print >> output, "}"
