#!/usr/bin/env python2

"""
Copyright (c) 2014, 2020 Pelle Nilsson

To the extent possible under law, Pelle Nilsson has waived all copyright and
related or neighboring rights to gamebookformat. This work is published from:
Sweden.

http://creativecommons.org/publicdomain/zero/1.0/
"""

import os
import os.path
import sys
import json

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

def check_report(msg):
    print "%s: %s" % (sys.argv[len(sys.argv)-1], msg)

found_errors = False # yay, global state
def check_error(msg):
    check_report(msg)
    global found_errors
    found_errors = True

def check_all_sections_can_be_reached_in_theory(sections, references):
    reached = set()
    traverse(sections, references, traverse_add, reached)
    for section in sections:
        if section not in reached:
            check_error("Could not reach section '%s' from start." % section)

def report_all_ending_sections(sections, references):
    ending_sections = []
    for section in sections:
        if len(references[section]) == 0:
            ending_sections.append(section)
    for ending_section in ending_sections:
        check_report("ending (death?) section found: %s" % ending_section)

def parse_book(inputfilename):
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
    return [sections, references]

def verbose_report_gamebook(sections, references):
    report_all_ending_sections(sections, references)

def check_gamebook(inputfilename, verbose):
    [sections, references] = parse_book(inputfilename)
    check_all_sections_can_be_reached_in_theory(sections, references)
    if verbose:
        verbose_report_gamebook(sections, references)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('inputfile', metavar='debugfile',
                    help='input gamebook JSON file (eg test.json)')
    ap.add_argument('-v', '--verbose', action='store_true',
                    dest='verbose',
                    help='verbose output')
    args = ap.parse_args()
    check_gamebook(args.inputfile, args.verbose)
    if found_errors:
        sys.exit(1)
    else:
        sys.exit(0)
