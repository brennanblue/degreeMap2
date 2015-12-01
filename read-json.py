#!/usr/bin/env python

import sys
import json
import urllib2
import argparse
from collections import namedtuple, Counter
# from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedList)
# help(SortedSet)
# help (SortedDict)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument('--debug', '-d', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    if args.debug:
        DEBUG = True
    else:
        DEBUG = False

    if args.verbose:
        VERBOSE = True
    else:
        VERBOSE = False

    # Read file
    with open(args.filename, 'r') as json_file:
        contents = json_file.read()
        choices = json.loads(contents)

    # Make sure that worked
    if not choices:
        sys.stderr.write("Error reading json file\n")
        sys.exit()

    # dictionaries for courses, subjects
    courses = {}
    course_meta = {'alpha':None, 'course': None, 'number': None, 'credits': None} #, 'colleges':[]}
    #dictionary - use keyed index as with known, fetch detail
    course_detail = {'type': None, 'title': None, 'desc':None, 'pre':None }
    subjects = {} # dictionary / set
    manifest = {} # new for 11/30
    courselist = [] # list / array
    subjlist = [] # list / array
    chosen_courses = []
    n = 0
    slot = 0 #iterators
    # parse = False

    for i in choices: 
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            # parse = True
            course_meta['course'] = str(choices[i][-9:].strip())
            parts = course_meta['course'].split("_")
            subjects[n] = [parts[1]]
            course = "{} {}".format(parts[0], parts[1])
            subj = "{}".format(parts[0])
            course_meta['number'] = str(parts[1])
            course_meta['alpha'] = str(parts[0])
            courses[slot] = course_meta
            chosen_courses.append(course)
            courselist.append(course)
            subjlist.append(subj)
            coursedetail = getCourse(course)
            if VERBOSE:
                print "{}  - [course] \n\r ".format (coursedetail)
            if DEBUG:
                subj_catalog = fetch(subj)
                print "Prepare for it.... \n\r {}".format(subj_catalog)
            for detail in coursedetail:
                print detail
            # course_title = str(coursedetail['course_title'])
            # course_detail['title'] = course_title
            # colleges = str(coursedetail['college'])
            # course_meta['colleges'] = colleges.split("/")
            # course_detail['desc'] = str(coursedetail['description'])
            # if (len(coursedetail['credits']) > 1 ):
            #     course_credits = int(coursedetail['credits'])
            # else:
            #     course_credits = str(coursedetail['credits'])
            #     range = course_meta['credits'].split("-")
            #     low = int(range[0].strip)
            #     high = int(range[1].strip)
            # alpha = str(coursedetail['alpha'])
            # contact_type = str(coursedetail['alpha'])
            # description, pre = desc.split(" Pre: ")
            #     #do some tuple packing!
            # tag = (subj, course, hours)
            # meta = (contact_type, college)
            # if desc == description:
            #     detail = (title, desc)
            # else:
            #     detail = (title, description, pre)

            # manifest[course] = (tag, detail, meta)
            # print pre


        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                # parse = True
                course_meta['course'] = choices[i][-9:].strip()
                parts = course_meta['course'].split("_")
                subjects[n] = (parts[1], parts[0])
                course = "{} {}".format(parts[0], parts[1])
                subj = "{}".format(parts[0])
                course_meta['number'] = str(parts[1])
                course_meta['alpha'] = str(parts[0])
                courses[slot] = course_meta
                courselist.append(course)
                subjlist.append(subj)
                chosen_courses.append(course)
                coursedetail = getCourse(course)
                for detail in coursedetail:
                    print detail
                if VERBOSE:
                    print "{}  - [course] \n\r ".format (coursedetail)
                if DEBUG:
                    subj_catalog = fetch(subj)
                    print "Prepare for it.... \n\r {}".format(subj_catalog)
                # title = str(coursedetail['course_title'])
                # desc = str(coursedetail['description'])
                # if (len(coursedetail['credits']) > 1 ):
                #     credits = int(coursedetail['credits'])
                # else:
                #     credits = str(coursedetail['credits'])
                #     range = credits.split("-")
                #     low = int(range[0].strip)
                #     high = int(range[1].strip)
                # alpha = str(coursedetail['alpha'])
                # contact_type = str(coursedetail['alpha'])
                # colleges = str(coursedetail['college'])
                # college = colleges.split("/")
                # description, pre = desc.split(" Pre: ")
                #     #do some tuple packing!
                # tag = (subj, course, hours)
                # meta = (contact_type, college)
                # if desc == description:
                #     detail = (title, desc)
                # else:
                #     detail = (title, description, pre)
                # manifest[course] = (tag, detail, meta)
                # print pre


        # if(parse):
        #     coursetuple = (subj, courses[slot])
        #     chosen[n] = coursetuple
        #     subjlist.append(subj)
        # parse or not, continue iterating 
        # n += 1
    print manifest

    choices = Choices(subjlist, courselist) #replace raw json input with cleaned python object
    print "There are {} slots with courses specified".format(slot)

    # subjlist = False
    # courselist = False

    order = sorted(choices.courselist, key = lambda x: x[1], reverse=True)
    print "The following courses were chosen\n\r {} \t".format(order)

    # for i in courses:
    #     print chosen_courses[i-1]

    uber = {}
    ranked_subj = [[x,choices.subjlist.count(x)] for x in set(choices.subjlist)]
    for subj in ranked_subj:
        # print "{} courses with alpha".format(subj[0]) #, subj.count(ranked_subj))
        # uber["subject"] = subj[0]
        # subj_courses = {}
        # coursetally =[]
        # for course in courselist:
        #     if subj[0] in course:
        #         coursetally.append(course)
        #         courselist.remove(course)

        uber["courses"] = (subj[0],subj[1])
        uber["detail"] = ()
        print uber

    chosen = set(chosen_courses)
    for choice in chosen:

        print "{}\t".format(choice)

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
    # print url
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data

def getCoursePrereqs(alpha, number):
    url = "http://webdev.uhh.hawaii.edu/timeline/courses/_{}.json".format(alpha)
    response = urllib2.urlopen(url)
    data = json.load(response)
    #drill 


########################## Choices Class - extract?####
class Choices(object):
    def __init__(self,list_of_subjects, list_of_courses):
        self.courselist = list_of_courses
        self.subjlist = list_of_subjects
        # self.credit_hours = courses_by_credits

if __name__ == '__main__':
    main()