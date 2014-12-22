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

def twine2(s):
    #have to think of a good solution
    return (s.replace("`", "'")
            .replace("<", " `<` ")
            .replace(">", " `>` ")
            .replace("&", " `&` ")
            .replace("\r\n", " ")
            .replace("\n", " ")
            .replace("[", " `[` ")
            .replace("]", " `]` "))

def no(s):
    return s
