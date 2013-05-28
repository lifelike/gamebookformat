from output import OutputFormat

class DotFormat (OutputFormat):
    def __init__(self):
        super(DotFormat, self).__init__('dot', 'Graphviz paragraph flowchart')


