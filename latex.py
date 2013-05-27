from output import OutputFormat

DEFAULT_DOCUMENT_START = """
\\documentclass[a4,onecolumn]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[hidelinks]{hyperref}

\\usepackage[top=3.3cm, bottom=3.3cm, left=2cm, right=2cm]{geometry}

\\newif\\ifpdf
\\ifx\\pdfoutput\\undefined
  \\pdffalse
\\else
  \\ifnum\\pdfoutput=1
    \\pdftrue
  \\else
    \\pdffalse
  \\fi
\\fi

\\title{Gamebook}
\\author{}
\\date{}

\\begin{document}

\\thispagestyle{empty}
\\clearpage

"""

def format_latex_paragraph_ref(paragraph, shuffled_paragraphs):
    return ("\\textbf{%d}" % shuffled_paragraphs.to_nr[paragraph])

class LatexFormat (OutputFormat):
    def __init__(self):
        super(LatexFormat, self).__init__('tex', 'LaTeX')

    def write_begin(self, book, output):
        print >> output, DEFAULT_DOCUMENT_START

    def write_paragraph(self, paragraph, shuffled_paragraphs, output):
        print >> output, " \\noindent"
        print >> output, format_latex_paragraph_ref(paragraph,
                                                    shuffled_paragraphs)
        print >> output, " -- "
        print >> output, paragraph.format(shuffled_paragraphs,
                                          format_latex_paragraph_ref)
        print >> output, "\\newline"
        print >> output

    def write_end(self, book, output):
        print >> output, "\end{document}"
