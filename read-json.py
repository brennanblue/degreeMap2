#!/usr/bin/env python

import sys
import json
import argparse
# from collections import namedtuple

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
    l = []
    for i in choices: 
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            courses[slot] = choices[i][-9:].strip()
            parts = courses[slot].split("_")
            subjects[parts[1]] = parts[0]
            string = "{} {}".format(parts[0], parts[1])
            l.append(string)
            # subjects[parts[0]].append(subjects[parts[1]])
        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                courses[slot] = choices[i][-9:].strip()
                parts = courses[slot].split("_")
                subjects[parts[1]] = parts[0]
                string = " %s: - %s; " % (parts[0], parts[1])
                l.append(string)

    print "There are {} slots with courses specified".format(slot)

    s = "\n".join(l)
    print s

    print "A total of {} courses were chosen".format(len(courses))

def isset(variable):
    return variable in locals() or variable in globals()

##########################

if __name__ == '__main__':
    main()