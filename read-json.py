#!/usr/bin/env python

import sys
import json
import argparse
from collections import namedtuple, Counter

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()

    if args.debug:
        DEBUG = True
    else:
        DEBUG = False

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
    courses = []
    chosen_courses = []
    courselist = [] #list
    subjlist = [] #list
    chosen = {} #dictionary
    n = 0
    parse = False

    for i in choices: 
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            parse = True
            guts = choices[i][-9:].strip()
            courses.append(guts)
        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                parse = True
                guts = choices[i][-9:].strip()
                courses.append(guts)
        if(parse):
            # courses.append(int(slot))
            courses.append(choices[i][-9:].strip())
            parts = courses[slot].split("_")
            # for x in parts:
            # print "Subj {}; Course is {}".format(parts[0], parts[1])
            # coursenum = str(parts[1])
            # subj = str(parts[0])
            # coursetuple = (subj, coursenum)
            # chosen_courses.append(coursetuple)
            # courselist.append(coursenum)
            # subjlist.append(subj)
        #parse or not, continue iterating 
        n += 1

    choices = Choices(subjlist, courselist) #replace raw json input with cleaned python object

    print "There are {} slots with courses specified".format(slot)

    if(DEBUG):
        for x in chosen_courses: #prints each subject
            print chosen_courses[x]

    ranked_subj = [[x,subjlist.count(x)] for x in set(subjlist)]

    for subj in ranked_subj:
        print "{} courses with {} alpha".format(ranked_subj[subj],subj)

    for x in choices.subjlist:
        print "Subject is {}, Course is".format(x)

    if(DEBUG):
        tallyed_list = sorted(subjlist, key = lambda x: x[1], reverse=True)
        print "tallyed_list is: {} \n".format(tallyed_list)

    # rank = Counter(subjects)
    # print "rank variable is: {} \n".format(rank)

    print "The following courses were chosen {}".format(courses)


#list filter 
# l = [x for x in l if x != 0]

############# FUNC - store elsewhere? ###############

def isset(variable):
    return variable in locals() or variable in globals()

def fetch(course):  #returns object
    url = "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(course)
    # Parse JSON into an object with attributes corresponding to dict keys.
    data = json.loads(data, object_hook=lambda d: namedtuple('course', d.keys())(*d.values()))
    return data


########################## Choices Class - extract?####
class Choices(object):
    def __init__(self,list_of_subjects, list_of_courses):
        self.courselist = list_of_courses
        self.subjlist = list_of_subjects


if __name__ == '__main__':
    main()