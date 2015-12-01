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
            coursedetail = getCourse(course_meta['course'])
            dir(coursedetail)
            # info(coursedetail)
            # print "Course Title is {}".format(coursedetail)

            if VERBOSE:
                print "{}  - [course] \n\r ".format (coursedetail)
            if DEBUG:
                subj_catalog = fetch(subj)
                print "Prepare for it.... \n\r {}".format(subj_catalog)
            
            for i, detail in enumerate(coursedetail):
                print "Index is {}, data is {}".format(i, detail)

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
                coursedetail = eval(getCourse(course))
                # print "{}".format(getCourseDetail(course)) # works as string
                course_obj = str_to_course_obj(getCourseDetail(course))
                print course_obj
                for detail in course_obj:  # not iterable.
                    print detail

                if VERBOSE:
                    print "{}  - [course] \n\r ".format (coursedetail)
                if DEBUG:
                    subj_catalog = fetch(subj)
                    print "Prepare for it.... \n\r {}".format(subj_catalog)
               

    ECON_131 = CourseObj.parse("Econ / Econ 131 / Intro to Microeconomics / 3")
    print "{}".format(ECON_131)

    choices = Choices(subjlist, courselist) #replace raw json input with cleaned python object
    print "There are {} slots with courses specified".format(slot)

    # subjlist = False
    # courselist = False

    order = sorted(choices.courselist, key = lambda x: x[1], reverse=True)
    print "The following courses were chosen\n\r {} \t".format(order)

    uber = {}
    ranked_subj = [[x,choices.subjlist.count(x)] for x in set(choices.subjlist)]
    for subj in ranked_subj:

        uber["courses"] = (subj[0],subj[1])
        uber["detail"] = ()
        print uber

    chosen = set(chosen_courses)
    for choice in chosen:

        print "{}\t".format(choice)

    if(DEBUG):

        subjtally = sorted(choices.subjlist, key = lambda x: x[1], reverse=True)
        print "The sorted subject list is: {} \n".format(subjtally)

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

def getCourseDetail(coursenum):  # returns object of type course
    url = "http://hilo.hawaii.edu/courses/api/1.1/course/{}".format(coursenum)
    response = urllib2.urlopen(url)
    data = json.load(response)
    for attrib, attrib_data in enumerate(data):
        print "attrib = {}, attrib_data = {}\n".format(attrib,attrib_data)
    return data

def getCoursePrereqs(alpha, number):
    url = "http://webdev.uhh.hawaii.edu/timeline/courses/_{}.json".format(alpha)
    response = urllib2.urlopen(url)
    data = json.load(response)
    #drill 

def str_to_course_obj(str):
    return reduce(getattr, str.split("."), sys.modules[__name__])

def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])

########################## Choices Class - extract?####
class Choices(object):
    def __init__(self,list_of_subjects, list_of_courses):
        self.courselist = list_of_courses
        self.subjlist = list_of_subjects
        # self.credit_hours = courses_by_credits

class course_obj:
    pass

class CourseObj(object):
    def __init__(self, subj, name, title, credits): #, description, college, contact_type):
        self.subj = subj
        self.name = name
        self.title = title
        self.credits = credits
        # self.desc = description
        # self.college = college
        # self.type = contact_type

    @classmethod
    def parse(cls, s):
        # some input validation here would be a good idea
        subj,name,title,credits = s.split('/')
        credits = int(credits)
        return cls(subj, name, title, credits)

if __name__ == '__main__':
    main()