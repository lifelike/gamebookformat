#FIXME entire file is a hack

def latex(s):
    return (s.replace('\\', '\\textbackslash')
            .replace('&', '\&')
            .replace('%', '\%')
            .replace('$', '\$')
            .replace('#', '\#')
            .replace('_', '\_')
            .replace('{', '\{')
            .replace('}', '\}')
            .replace('~', '\\textasciitilde')
            .replace('^', '\\textasciicircum'))

def rtf(s):
    return (s.replace('\\', '\\\\')
            .replace('{', '\\{')
            .replace('}', '\\}'))

import cgi

def html(s):
    return cgi.escape(s)

def js(s):
    return (s.replace("\\", "\\\\")
            .replace('"', '\\"'))


def no(s):
    return s
