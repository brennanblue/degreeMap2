#!/usr/bin/env python

import sys
import json
import urllib2
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

    # dictionaries for courses, subjects
    courses = {} #dictionary / list
    subjects = {} # dictionary / set
    courselist = [] # list / array
    subjlist = [] # list / array
    n = 0
    slot = 0 #iterators
    # parse = False

    for i in choices: 
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            # parse = True
            courses[slot] = choices[i][-9:].strip()
            parts = courses[slot].split("_")
            subjects[n] = [parts[1]]
            course = "{} {}".format(parts[0], parts[1])
            subj = "{}".format(parts[0])
            courselist.append(course)
            subjlist.append(subj)
            coursedetail = getCourse(courses[slot])
            print "{}  - [course] \n\r ".format (coursedetail)
            if DEBUG:
                subj_catalog = fetch(subj)
                print "Prepare for it.... \n\r {}".format(subj_catalog)

        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                # parse = True
                courses[slot] = choices[i][-9:].strip()
                parts = courses[slot].split("_")
                subjects[n] = (parts[1], parts[0])
                course = "{} {}".format(parts[0], parts[1])
                subj = "{}".format(parts[0])
                courselist.append(course)
                subjlist.append(subj)
                coursedetail = getCourse(course)

                print "{}  - [course] \n\r ".format (coursedetail)
                if DEBUG:
                    subj_catalog = fetch(subj)
                    print "Prepare for it.... \n\r {}".format(subj_catalog)

        # if(parse):
        #     coursetuple = (subj, courses[slot])
        #     chosen[n] = coursetuple
        #     subjlist.append(subj)
        # parse or not, continue iterating 
        n += 1

    choices = Choices(subjlist, courselist) #replace raw json input with cleaned python object
    print "There are {} slots with courses specified".format(slot)

    order = sorted(choices.courselist, key = lambda x: x[1], reverse=True)
    print "The following courses were chosen\n\r {} \t".format(order)

    ranked_subj = [[x,choices.subjlist.count(x)] for x in set(choices.subjlist)]
    for subj in ranked_subj:
        print "{} courses with alpha".format(subj) #, subj.count(ranked_subj))

    if(DEBUG):

        subjtally = sorted(choices.subjlist, key = lambda x: x[1], reverse=True)
        print "The sorted subject list is: {} \n".format(subjtally)

#list filter 
# l = [x for x in l if x != 0]

############# FUNC - store elsewhere? ###############

def isset(variable):
    return variable in locals() or variable in globals()

def fetch(alpha):  #returns object
    subjurl =  "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(alpha)
    # Parse JSON into an object with attributes corresponding to dict keys.
    response = urllib2.urlopen(subjurl)
    data = json.load(response) 
    # choices = json.loads(contents)
    # data = json.loads(data, object_hook=lambda d: namedtuple('course', d.keys())(*d.values()))
    return data

def getCourse(coursenum): # returns course detail
     url = "http://hilo.hawaii.edu/courses/api/1.1/course/{}".format(coursenum)
     print url
     response = urllib2.urlopen(url)
     data = json.load(response)
     return data

########################## Choices Class - extract?####
class Choices(object):
    def __init__(self,list_of_subjects, list_of_courses):
        self.courselist = list_of_courses
        self.subjlist = list_of_subjects

if __name__ == '__main__':
    main()