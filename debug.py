from output import OutputFormat

class DebugFormat (OutputFormat):
    def __init__(self):
        super(DebugFormat, self).__init__('debug', 'Gamebook Debug Output')
