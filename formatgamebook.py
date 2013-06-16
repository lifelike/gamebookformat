#!/usr/bin/env python2

"""
Copyright (c) 2013, Pelle Nilsson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in
the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import re
import os
import os.path
import sys
import json

import quote
import sections
import templates
from output import OutputFormat

USAGE = "usage: %prog [options] inputfile(s)... outputfile"

SECTION_NAME_RE = re.compile("^[a-z][a-z_0-9]*$")

def of(extension, name, quote):
    return {'extension' : extension,
            'name' : name,
            'quote' : quote
    }

OUTPUT_FORMATS = [
    of('tex', 'LaTeX', quote.latex),
    of('rtf', 'Rich Text Format', quote.rtf),
    of('dot', 'Graphviz section flowchart', quote.no),
    of('html', 'HTML+JS playable in browser', quote.html),
    of('txt', 'Plain text', quote.no),
    of('debug', 'Gamebook Debug Output', quote.no),
]

def make_supported_formats_list_string():
    return "Supported Output Formats:\n" + "\n".join(
        [' %-8s%s' % (f['extension'], f['name'])
         for f in OUTPUT_FORMATS])

def format_gamebook(inputfilenames,
                    outputfilename,
                    import_default_map_file,
                    templatedirs,
                    shuffle):
    output_format = make_output(outputfilename, templatedirs)
    book = sections.Book(make_bookid(outputfilename))
    for inputfilename in inputfilenames:
        parse_file_to_book(open(inputfilename, 'r'), book)
    if import_default_map_file:
        import_default_nr_map(outputfilename, book)
    write_book(book, shuffle, output_format, outputfilename)

def make_bookid(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def parse_file_to_book(inputfile, book):
    before_first_section = True
    name = None
    number = None
    text = ""
    tags = None
    intro_section = False
    for line in inputfile.readlines():
        if line.startswith('*'):
            before_first_section = False
            if name:
                add_section_to_book(book, name, text, intro_section, number,
                                    tags)
            number = None
            text = ""
            intro_section = False
            heading = [h.strip() for h in line[1:].strip().split()]
            if len(heading) > 1 and heading[-1].startswith(':'):
                if not heading[-1].endswith(':'):
                    raise Exception('Section heading tags syntax error: %s' %
                                    heading)
                tags = [t.strip() for t in heading[-1][1:-1].split(':')]
                heading = heading[:-1]
            else:
                tags = None
            if len(heading) == 1:
                name = heading[0]
            elif len(heading) == 2:
                number = int(heading[0])
                name = heading[1]
            if not name or not SECTION_NAME_RE.match(name):
                raise Exception("bad section heading: %s" % str(heading))
        elif line.startswith('='):
            if name:
                add_section_to_book(book, name, text, intro_section, number)
            name = line[1:].strip()
            intro_section = True
            text = ""
        elif before_first_section and '=' in line:
            config = line.split('=')
            book.configure(config[0].strip(), config[1].strip())
        elif name:
            text = text + " " + line.strip()
        elif len(line.strip()):
            raise Exception("unknown content before sections: %s"
                            % line.strip())
    if name:
        add_section_to_book(book, name, text, intro_section, number, tags)

def add_section_to_book(book, name, text, intro_section=False,
                        number=None, tags=None):
    section = sections.Section(name, text)
    if tags:
        section.add_tags(tags)
    if intro_section:
        book.addintro(section)
    else:
        book.add(section)
        if number:
            book.force_section_nr(name, number)

def make_output(outputfilename, templatedirs):
    for of in OUTPUT_FORMATS:
        extension = of['extension']
        if outputfilename.endswith('.' + extension):
            return OutputFormat(templates.Templates(templatedirs, extension),
                                of['quote'])
    raise Exception("Unsupported or unknown output format for %s."
                    % outputfilename)

def write_book(book, shuffle, output_format, outputfilename):
    shuffled_sections = book.shuffle(shuffle)
    output = open(outputfilename, 'w')
    print >> output, output_format.format_begin(book.config),
    print >> output, output_format.format_intro_sections(book.introsections,
                                                  shuffled_sections)
    print >> output, output_format.format_sections_begin(book.config),
    print >> output, output_format.format_shuffled_sections(shuffled_sections),
    print >> output, output_format.format_end(book.config),
    save_section_mapping(shuffled_sections, outputfilename)

def import_default_nr_map(outputfilename, book):
    mapfilename = make_default_map_filename(outputfilename)
    if os.path.exists(mapfilename): #FIXME better check
        for name,nr in json.load(open(mapfilename)).iteritems():
            book.force_section_nr(name, nr)

def save_section_mapping(shuffled_sections, outputfilename):
    mapfilename = make_default_map_filename(outputfilename)
    json.dump(shuffled_sections.name_to_nr, open(mapfilename, 'w'))

def make_default_map_filename(outputfilename):
    basename = outputfilename
    dotpos = outputfilename.rfind('.')
    if dotpos >= 1:
        basename = outputfilename[:dotpos]
    return basename + '.map'

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(epilog=make_supported_formats_list_string(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputfiles', metavar='inputfile', nargs='+',
                    help='input gamebook file (eg test.gamebook)')
    ap.add_argument('outputfile', metavar='outputfile',
                    help='output file (eg test.tex or test.rtf)')
    ap.add_argument('-M', '--no-default-map', action='store_false',
                    dest='import_default_map_file',
                    help='ignore default map file')
    ap.add_argument('-t', '--template', metavar='D', dest='templatedirs',
                    action='append', help='add custom template dir')
    ap.add_argument('-S', '--no-shuffle', action='store_false',
                    dest='shuffle',
                    help='do not shuffle sections')
    args = ap.parse_args()
    templatedirs = ['templates',
                    os.path.join(os.path.dirname(sys.argv[0]), 'templates')]
    if args.templatedirs:
        for t in args.templatedirs:
            templatedirs.insert(-2, t)
    format_gamebook(args.inputfiles,
                    args.outputfile,
                    args.import_default_map_file,
                    templatedirs,
                    args.shuffle)
