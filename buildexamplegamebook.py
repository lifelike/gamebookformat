#!/usr/bin/env python

import os
import sys

DEFAULT_OPTIONS = '--no-shuffle'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >> sys.stderr, "usage: %s infile outfile" % sys.argv[0]
        sys.exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    print infile, outfile
    optionsfilename = infile + '.options'
    options = DEFAULT_OPTIONS
    if os.path.exists(optionsfilename):
        optionsfile = open(optionsfilename)
        options += ' ' + ' '.join(optionsfile.readlines())
        optionsfile.close()
    os.system("python ./formatgamebook.py %s %s %s" % (
        options, infile, outfile))
