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

    # else:
    #     if a.broken:
    #         print "i is {}, choices[i] is {}\r\n".format(i, courses[i])

    # choices = Choices(subj, courselist)
    # # replace raw json input with cleaned python object
    # print "There were {} slots with courses specified".format(slot)

    # order = sorted(choices.courselist, key=lambda x: x[1], reverse=True)
    # print "The following courses were chosen\n\r {} \t".format(order)

    # # Parse JSON into an object with attributes corresponding to dict keys.
    # # x = json.loads(
    # # data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # # print x.name, x.hometown.name, x.hometown.id

    # if a.debug:
    #     uber = {}
    #     ranked_subj = [[x, choices.subjlist.count(x)] for x in set(
    #         choices.subjlist)]
    #     for subj in ranked_subj:
    #         uber["courses"] = (subj[0], subj[1])
    #         # uber["detail"] = ()
    #         print uber

    # if(a.debug):

    #     sbj_tlly = sorted(choices.subjlist, key=lambda x: x[1], reverse=True)
    #     print "The sorted subject list is: {} \n".format(sbj_tlly)


# ############ FUNC - store elsewhere? ############## #

def isset(variable):
    return variable in locals() or variable in globals()


def pop_meta(coursenum):  # returns object
    # course = get_course(coursenum)
    parts = coursenum.split("_")
    str_course = "{} {}".format(parts[0], parts[1])
    crse_meta = {
        'course': None, 'type': None, 'credits': None,
        'college': None, 'xlist': None, 'colleges': []}
    crse_meta['course'] = str_course

# def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
# def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

# x = json2obj(data)  sample call of above

# ######################### Choices Class - extract?####


class Choices(object):
    def __init__(self, list_of_subjects, list_of_courses):
        self.courselist = list_of_courses
        self.subj = list_of_subjects
        # self.credit_hours = courses_by_credits


class CourseObj(object):
    def __init__(self, subj, name, title, credits):
        # description, college, contact_type):
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
        subj, name, title, credits = s.split('/')
        credits = int(credits)
        return cls(subj, name, title, credits)

if __name__ == '__main__':
    main()
