#!/usr/bin/env python2

import sys
import json

import paragraphs

from output import OutputFormat
from latex import LatexFormat
from rtf import RtfFormat
from dot import DotFormat
from debug import DebugFormat

USAGE = "usage: %prog [options] inputfile(s)... outputfile"

OUTPUT_FORMATS = [LatexFormat(),
                  RtfFormat(),
                  DotFormat(),
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

