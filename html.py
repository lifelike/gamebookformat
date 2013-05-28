from output import OutputFormat

class HtmlFormat (OutputFormat):
    def __init__(self):
        super(HtmlFormat, self).__init__('html',
                                         'HTML+JS playable in browser')
