from output import OutputFormat

class LatexFormat (OutputFormat):
    def __init__(self):
        super(LatexFormat, self).__init__('tex', 'LaTeX')
