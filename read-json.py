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

    courses = {} #dictionary / list
    # chosen_courses = {}
    subjects = {} # list?
    # alphas = [] # array?
    courselist = []
    subjlist = []
    # chosen = []

    # courses = []
    # chosen_courses = {}
    # courselist = [] #list
    # subjlist = [] #list
    # chosen = {} #dictionary
    n = 0
    parse = False

    for i in choices: 
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            parse = True
            courses[slot] = choices[i][-9:].strip()
            parts = courses[slot].split("_")
            subjects[n] = [parts[1]]
            string = "{} {}".format(parts[0], parts[1])
            subj = "{}".format(parts[0])
            # coursetuple = (subj, courses[slot])

            # chosen_courses[subj] = string 
                       # chosen[n] = string
            # chosen.append(coursetuple)
            courselist.append(string)
            subjlist.append(subj)
            
            # guts = choices[i][-9:].strip()
            # courses.append(guts)
        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                # parse = True
                # guts = choices[i][-9:].strip()
                # courses.append(guts)

                courses[slot] = choices[i][-9:].strip()
                parts = courses[slot].split("_")
                subjects[i] = (parts[1], parts[0])
                string = "{} {}".format(parts[0], parts[1])
                subj = "{}".format(parts[0])
                # coursetuple = (subj, courses[slot])
                # chosen[n] = coursetuple
                # courselist.append(string)
                subjlist.append(subj)

        # if(parse):
        #     courses[slot] = choices[i][-9:].strip()
        #     parts = courses[slot].split("_")
        #     subjects[i] = (parts[1], parts[0])
        #     string = "{} {}".format(parts[0], parts[1])
        #     subj = "{}".format(parts[0])
        #     coursetuple = (subj, courses[slot])
        #     chosen[n] = coursetuple
        #     courselist.append(string)
        #     subjlist.append(subj)
        # parse or not, continue iterating 
        n += 1

    choices = Choices(subjlist, courselist) #replace raw json input with cleaned python object

    print "There are {} slots with courses specified".format(slot)

    ranked_subj = [[x,subjlist.count(x)] for x in set(subjlist)]

    for subj in ranked_subj:
        print "{} courses with alpha".format(subj) #, subj.count(ranked_subj))

    courses = sorted(choices.courselist, key = lambda x: x[1], reverse=True)
    print "The following courses were chosen\n\r {} \t".format(courses)

    if(DEBUG):

        subjects = set(choices.subjlist)
        for x in subjects: #prints each subject
            print "The sorted subject list is: \n {} \t".format(x)

        subjtally = sorted(choices.subjlist, key = lambda x: x[1], reverse=True)
        subjset = set(subjtally)
        print "The sorted cubject list is: {} \n".format(subjset)

    # rank = Counter(subjects)
    # print "rank variable is: {} \n".format(rank)




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