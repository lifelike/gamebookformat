#!/usr/bin/env python2

"""
Copyright (c) 2014, Pelle Nilsson
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

USAGE = "usage: %prog [options] inputfile(s)... outputfile"

def find_section_nr_names(sections):
    section_nr_to_name = {}
    for section_name,section_contents in sections.iteritems():
        section_nr_to_name[section_contents["nr"]] = section_name
    return section_nr_to_name

def find_references(sections):
    section_nr_to_name = find_section_nr_names(sections)
    references = {}
    for section_name,section_contents in sections.iteritems():
        references_from_section = []
        for t in section_contents["text"]:
            if isinstance(t, dict) and "reference" in t:
                ref = section_nr_to_name[int(t["reference"])]
                references_from_section.append(ref)
        references[section_name] = references_from_section
    return references

def traverse(sections, references, function, data):
    stack = ["start"]
    visited = set()
    while len(stack) > 0:
        section = stack.pop()
        function(section, data)
        visited.add(section)
        for reference in references[section]:
            if reference not in visited:
                stack.append(reference)

def traverse_add(section, data):
    data.add(section)

found_errors = False # yay, global state
def check_error(msg):
    print "%s: %s" % (sys.argv[1], msg)
    global found_errors
    found_errors = True

def check_all_sections_can_be_reached_in_theory(sections, references):
    reached = set()
    traverse(sections, references, traverse_add, reached)
    for section in sections:
        if section not in reached:
            check_error("Could not reach section '%s' from start." % section)

def check_gamebook(inputfilename):
    book = json.load(open(inputfilename))
    sections = book["sections"]
    if not "start" in sections:
        check_error("No start section found. Cancelling checks.")
        sys.exit(1)
    del sections["IGNORE-debug-json-padding-IGNORE"]
    for section in sections.keys():
        if section.startswith("empty-"):
            del sections[section]
    references = find_references(sections)
    check_all_sections_can_be_reached_in_theory(sections, references)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputfile', metavar='debugfile',
                    help='input gamebook debug file (eg test.debug)')
    args = ap.parse_args()
    check_gamebook(args.inputfile)
    if found_errors:
        sys.exit(1)
    else:
        sys.exit(0)
