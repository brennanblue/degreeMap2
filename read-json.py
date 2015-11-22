#!/usr/bin/env python

import sys
import json
import argparse
from collections import namedtuple, Counter

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    # Read file
    with open(args.filename, 'r') as json_file:
        contents = json_file.read()
        choices = json.loads(contents)

    # Make sure that worked
    if not choices:
        sys.stderr.write("Error reading json file\n")
        sys.exit()

    #iterator
    slot = 0

    # dictionaries for courses, subjects
    courses = {}
    subjects = {}
    alphas = []
    courselist = []
    subjlist = []
    for i in choices: 
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            courses[slot] = choices[i][-9:].strip()
            parts = courses[slot].split("_")
            subjects[i] = [parts[1]]
            string = "{} {}".format(parts[0], parts[1])
            subj = "{}".format(parts[0])
            courselist.append(string)
            subjlist.append(subj)
            # alphas[parts[0]] = 1
            # subjects[i].append(subjects[parts[1]])
        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                courses[slot] = choices[i][-9:].strip()
                parts = courses[slot].split("_")
                subjects[i] = parts[1]

                string = " %s: - %s; " % (parts[0], parts[1])
                l.append(string)

    print "There are {} slots with courses specified".format(slot)

    s = "\n".join(courselist)
    print s

    q = '\n'.join(subjlist)
    print q

    print [[x,subjlist.count(x)] for x in set(subjlist)]

    rank = Counter(subjects)
    # Counter({'blue': 3, 'red': 2, 'yellow': 1})
    
    print "The following subjects were chosen {}".format(alphas)

def isset(variable):
    return variable in locals() or variable in globals()

def fetch(course):
    url = "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(course)

def fetchSubj(alpha):
    url = "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(alpha)
    return 
##########################

if __name__ == '__main__':
    main()