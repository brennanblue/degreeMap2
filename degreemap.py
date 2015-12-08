#!/usr/bin/env python

import sys
import json
import argparse  # url flags, filename variable
# import logging
import degreeparse
# import ast # string evaluator
# from collections import namedtuple

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--broken', '-b', action='store_true')
    parser.add_argument('--titles', '-t', action='store_true')

    a = parser.parse_args()

    # Read file
    with open(a.filename, 'r') as json_file:
        contents = json_file.read()
        io = json.loads(contents)
    # Make sure that worked
    if not io:
        sys.stderr.write("Error reading json file\n")
        sys.exit()

    # Transform imported data into structured data
    steps = degreeparse.ingest(io, a)
    print steps

    # order = sorted(choices.courselist, key=lambda x: x[1], reverse=True)
    # print "The following courses were chosen\n\r {} \t".format(order)

if __name__ == '__main__':
    main()
