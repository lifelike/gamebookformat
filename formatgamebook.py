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

import os
import os.path
import sys
import json

import sections
import templates
from output import OutputFormat

USAGE = "usage: %prog [options] inputfile(s)... outputfile"

def of(extension, name):
    return OutputFormat(templates.Templates(extension), extension, name)

OUTPUT_FORMATS = [
    of('tex', 'LaTeX'),
    of('rtf', 'Rich Text Format'),
    of('dot', 'Graphviz section flowchart'),
    of('html', 'HTML+JS playable in browser'),
    of('debug', 'Gamebook Debug Output'),
]

def make_supported_formats_list_string():
    return "Supported Output Formats:\n" + "\n".join(
        [str(f) for f in OUTPUT_FORMATS])

def format_gamebook(inputfilenames,
                    outputfilename,
                    import_default_map_file):
    output_format = find_output_format(outputfilename)
    book = sections.Book()
    for inputfilename in inputfilenames:
        parse_file_to_book(open(inputfilename, 'r'), book)
    if import_default_map_file:
        import_default_nr_map(outputfilename, book)
    write_book(book, output_format, outputfilename)

def parse_file_to_book(inputfile, book):
    name = None
    number = None
    text = ""
    for line in inputfile.readlines():
        if line.startswith('*'):
            if name:
                add_section_to_book(book, name, text, number)
            number = None
            text = ""
            heading = line[1:].strip().split(' ')
            if len(heading) == 1:
                name = heading[0]
            elif len(heading) == 2:
                number = int(heading[0])
                name = heading[1]
            else:
                raise Exception("bad section heading %s" % str(heading))
        else:
            text = text + " " + line.strip()
    if name:
        add_section_to_book(book, name, text, number)

def add_section_to_book(book, name, text, number=None):
    book.add(sections.Section(name, text))
    if number:
        book.force_section_nr(name, number)

def find_output_format(outputfilename):
    for of in OUTPUT_FORMATS:
        if of.supports(outputfilename):
            return of
    raise Exception("Unsupported or unknown output format for %s."
                    % outputfilename)

def write_book(book, output_format, outputfilename):
    shuffled_sections = book.shuffle()
    output = open(outputfilename, 'w')
    output_format.write_begin(book, output)
    output_format.write_shuffled_sections(shuffled_sections, output)
    output_format.write_end(book, output)
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
                    help='input gamebook file (eg test.json)')
    ap.add_argument('outputfile', metavar='outputfile',
                    help='output file (eg test.tex or test.rtf)')
    ap.add_argument('-M', '--no-default-map', action='store_false',
                    dest='import_default_map_file',
                    help='ignore default map file')
    args = ap.parse_args()
    format_gamebook(args.inputfiles,
                    args.outputfile,
                    args.import_default_map_file)

