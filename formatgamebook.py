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

import paragraphs

from output import OutputFormat
from latex import LatexFormat
from rtf import RtfFormat
from dot import DotFormat
from html import HtmlFormat
from debug import DebugFormat

USAGE = "usage: %prog [options] inputfile(s)... outputfile"

OUTPUT_FORMATS = [LatexFormat(),
                  RtfFormat(),
                  DotFormat(),
                  HtmlFormat(),
                  DebugFormat()]

def make_supported_formats_list_string():
    return "Supported Output Formats:\n" + "\n".join(
        [str(f) for f in OUTPUT_FORMATS])

def format_gamebook(inputfilenames, outputfilename):
    output_format = find_output_format(outputfilename)
    book = paragraphs.Book()
    for inputfilename in inputfilenames:
        parse_file_to_book(open(inputfilename, 'r'), book)
    output_format.write(book, open(outputfilename, 'w'))

def parse_file_to_book(inputfile, book):
    for name,contents in json.load(inputfile).iteritems():
        paragraph = paragraphs.Paragraph(name)
        if 'text' in contents:
            paragraph.addtext(contents['text'])
        if 'number' in contents:
            book.add(paragraph, contents['number'])
        else:
            book.add(paragraph)

def find_output_format(outputfilename):
    for of in OUTPUT_FORMATS:
        if of.supports(outputfilename):
            return of
    raise Exception("Unsupported or unknown output format for %s."
                    % outputfile)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(epilog=make_supported_formats_list_string(),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputfiles', metavar='inputfile', nargs='+',
                    help='input gamebook file (eg test.json)')
    ap.add_argument('outputfile', metavar='outputfile',
                    help='output file (eg test.tex or test.rtf)')
    args = ap.parse_args()
    format_gamebook(args.inputfiles, args.outputfile)

