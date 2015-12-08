#!/usr/bin/env python

import sys
import json  # data format
import urllib2  # fetch from API url
import argparse  # url flags, filename variable
import re  # regular expressions
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
        choices = json.loads(contents)

    # Make sure that worked
    if not choices:
        sys.stderr.write("Error reading json file\n")
        sys.exit()

    # dictionaries for courses, subjects
    # courses = {}
    crse_meta = {
        'course': None, 'type': None, 'credits': None,
        'college': None, 'xlist': None, 'colleges': []}
    # dictionary - use keyed index as with known, fetch detail
    crse_dtl = {
        'alpha': None, 'number': None, 'title': None,
        'desc': None, 'pre': None, 'prereqs': []}
    subjects = {}  # dictionary / set
    manifest = {}  # new for 11/30
    courselist = []  # list / array
    subjlist = []  # list / array
    n = 0
    slot = 0  # iterators

    for i in choices:
        # print i, choices[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            crse_meta['course'] = str(choices[i][-9:].strip())
            parts = crse_meta['course'].split("_")
            subjects[n] = [parts[1]]
            course = "{} {}".format(parts[0], parts[1])
            subj = "{}".format(parts[0])
            crse_dtl['number'] = str(parts[1])
            crse_dtl['alpha'] = str(parts[0])
            courselist.append(course)
            subjlist.append(subj)
            coursedetail = get_course(crse_meta['course'])

            # expandCourse(coursedetail,crse_meta,course_detail)

            description = str(coursedetail['description'])
            # need to have '_' seperator when querying API
            course_title = str(coursedetail['course_title'])
            if (len(coursedetail['credits']) > 1):
                course_credits = int(coursedetail['credits'])
            else:
                course_credits = str(coursedetail['credits'])
            print "\n\r[[[Slot {}]]]\n\r [ Course: ] \n\r\t{}: {} [{}]".format(
                slot, course, course_title, course_credits)

            colleges = str(coursedetail['college'])
            crse_meta['college'] = colleges
            crse_meta['colleges'] = colleges.split("/")
            if a.verbose:
                for college in crse_meta['colleges']:
                    print "College: {}\n".format(college)

            if 'Pre:' in description:
                parts = description.split(" Pre: ")
                crse_dtl['desc'] = parts[0]
                if parts[1]:
                    crse_dtl['pre'] = parts[1]
                    if '(Same as ' in parts[1]:
                        crse_dtl['pre'] = parts[0]
                        xlistparts = parts[1].split("Same as ")
                        cleaned = xlistparts[1].split(")")
                        print "X-listed with {}\n".format(cleaned[0])
                        prereq = xlistparts[0].split("(")
                        crse_dtl['pre'] = prereq[0].strip()
                        # remove cross list from prerequisite text
                    hits = re.search(
                        '([A-Z]{2-4})(?:\w?(\d{3}[A-Z]?))+', crse_dtl['pre'])
                    # this is the regex search .  Its failing.  Why?
                    if hits:
                        print("\n\r\n\r----PREREQS: {}----\n\r\n\r").format(
                            hits.group())
                else:
                    print "No Prereqs!"
                    crse_dtl['desc'] = description
                    crse_dtl['pre'] = False

            if '(Attributes:' in description:
                parts = description.split("(Attributes: ")
                if crse_dtl['pre']:  # if pre has attributes in it, clean it up
                    pre = crse_dtl['pre'].split("(Attributes: ")
                    crse_dtl['pre'] = pre[0].strip()
                if parts[1]:
                    print "[ Attributes: ]\n\r\t"
                    attrib = parts[1].split(")")
                    attr = attrib[0].split(", ")
                    for attrib in attr:
                        print "{}\t".format(attrib)
                crse_dtl['desc'] = parts[0]

            # after processing API data, fetch prereqs from alternate manifest
            if crse_dtl['pre']:
                crse_chain = get_prereq(crse_dtl['alpha'], crse_dtl['number'])
                if a.broken:
                    if crse_chain:
                        print crse_chain

            if a.titles:
                print "[ Description: ] \n\r\t {}".format(crse_dtl['desc'])

            if crse_dtl['pre']:
                pretext = crse_dtl['pre'].split(",")
                for p, pretxt in enumerate(pretext):
                    print "Prereq #{} is: {}\n\r".format(p, pretxt)
                # print "[ Prereq text: ]\n\r\t {}\n".format(crse_dtl['pre'])

            crse_dtl['title'] = course_title

            # alpha = str(coursedetail['alpha'])
            contact_type = str(coursedetail['contact_type'])

            if a.debug:
                print "{}  - [course] \n\r ".format(coursedetail)
            # if a.broken:
            #     subj_catalog = fetch(subj)
            #     print "Prepare for it.... \n\r {}".format(subj_catalog)

            # do some tuple packing!
            tag = (subj, course, course_credits)
            meta = (contact_type, colleges)

            detail = (course_title, description)
            manifest[course] = (tag, detail, meta)

            if a.debug:
                print manifest
                print tag

        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):

                slot += 1
                crse_meta['course'] = str(choices[i][-9:].strip())
                parts = crse_meta['course'].split("_")
                subjects[n] = [parts[1]]
                course = "{} {}".format(parts[0], parts[1])
                subj = "{}".format(parts[0])
                crse_dtl['number'] = str(parts[1])
                crse_dtl['alpha'] = str(parts[0])
                courselist.append(course)
                subjlist.append(subj)
                coursedetail = get_course(crse_meta['course'])
                # expandCourse(coursedetail,crse_meta,course_detail)
                description = str(coursedetail['description'])
                # need to have '_' seperator when querying API
                course_title = str(coursedetail['course_title'])
                if (len(coursedetail['credits']) > 1):
                    course_credits = int(coursedetail['credits'])
                else:
                    course_credits = str(coursedetail['credits'])
                print "\n\r[ Slot {} ]\n\r [ {} ]: \n\r\t {} [{}]".format(
                    slot, course, course_title, course_credits)

                colleges = str(coursedetail['college'])
                crse_meta['college'] = colleges
                crse_meta['colleges'] = colleges.split("/")
                if a.verbose:
                    for college in crse_meta['colleges']:
                        print "College: {}\n".format(college)

                if 'Pre:' in description:
                    parts = description.split(" Pre: ")
                    crse_dtl['desc'] = parts[0]
                    if parts[1]:
                        crse_dtl['pre'] = parts[1]
                        if '(Same as ' in parts[1]:
                            crse_dtl['pre'] = parts[0]
                            xlistparts = parts[1].split("Same as ")
                            cleaned = xlistparts[1].split(")")
                            print "X-listed with {}\n".format(cleaned[0])
                            prereq = xlistparts[0].split("(")
                            crse_dtl['pre'] = prereq[0].strip()
                            # remove cross list from prerequisite text
                    else:
                        print "No Prereqs!"
                        crse_dtl['desc'] = description
                        crse_dtl['pre'] = False

                if '(Attributes:' in description:
                    parts = description.split("(Attributes: ")
                    if crse_dtl['pre']:  # if pre has attributes, clean it.
                        pre = crse_dtl['pre'].split("(Attributes: ")
                        crse_dtl['pre'] = pre[0].strip()
                    if parts[1]:
                        print "[ Attributes: ]\n\r\t"
                        attrib = parts[1].split(")")
                        attr = attrib[0].split(", ")
                        for attrib in attr:
                            print "{}\t".format(attrib)
                    crse_dtl['desc'] = parts[0]

                # process API data, then fetch prereqs from alternate manifest
                if crse_dtl['pre']:
                    crse_chain = get_prereq(
                        crse_dtl['alpha'], crse_dtl['number'])
                    if a.broken:
                        if crse_chain:
                            print crse_chain

                if a.titles:
                    print "[ Description: ] \n\r\t {}".format(crse_dtl['desc'])

                if crse_dtl['pre']:
                    pretext = crse_dtl['pre'].split(",")
                    for p, pretxt in enumerate(pretext):
                        print "API Prereq #{} is: {}\n\r".format(p, pretxt)
                    # print "[ Prereqs: ]\n\r\t {}\n".format(crse_dtl['pre'])

                crse_dtl['title'] = course_title

                # alpha = str(coursedetail['alpha'])
                contact_type = str(coursedetail['contact_type'])

                if a.debug:
                    print "{}  - [course] \n\r ".format(coursedetail)

                # do some tuple packing!
                tag = (subj, course, course_credits)
                meta = (contact_type, colleges)

                detail = (course_title, description)
                manifest[course] = (tag, detail, meta)

                if a.debug:
                    print manifest
                    print tag

        # else:
        #     if a.broken:
        #         print "i is {}, choices[i] is {}\r\n".format(i, courses[i])

    choices = Choices(subjlist, courselist)
    # replace raw json input with cleaned python object
    print "There were {} slots with courses specified".format(slot)

    # subjlist = False
    # courselist = False

    order = sorted(choices.courselist, key=lambda x: x[1], reverse=True)
    print "The following courses were chosen\n\r {} \t".format(order)

    # Parse JSON into an object with attributes corresponding to dict keys.
    # x = json.loads(
    # data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # print x.name, x.hometown.name, x.hometown.id

    if a.debug:
        uber = {}
        ranked_subj = [[x, choices.subjlist.count(x)] for x in set(
            choices.subjlist)]
        for subj in ranked_subj:
            uber["courses"] = (subj[0], subj[1])
            # uber["detail"] = ()
            print uber

    if(a.debug):

        subjtally = sorted(choices.subjlist, key=lambda x: x[1], reverse=True)
        print "The sorted subject list is: {} \n".format(subjtally)


# ############ FUNC - store elsewhere? ############## #

def isset(variable):
    return variable in locals() or variable in globals()


def fetch(alpha):  # returns object
    subjurl = "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(alpha)
    # Parse JSON into an object with attributes corresponding to dict keys.
    response = urllib2.urlopen(subjurl)
    data = json.loads(response)
    # choices = json.loads(contents)
    # data = json.loads(data, object_hook=lambda d: namedtuple
    # course', d.keys())(*d.values()))
    return data


def get_course(coursenum):  # returns course detail
    url = "http://hilo.hawaii.edu/courses/api/1.1/course/{}".format(coursenum)
    # print url
    response = urllib2.urlopen(url)
    data = json.load(response)
    return data[0]


def get_prereq(alpha, number):  # returns course detail
    l = "http://webdev.uhh.hawaii.edu/timeline/courses/_{}.json".format(alpha)
    response = urllib2.urlopen(l)
    data = json.load(response)
    return_data = False
    if data['courses']:
        for crse_dtl in data['courses']:
            if crse_dtl['number'] == number:
                # print crse_dtl
                for attrib in crse_dtl:
                    if attrib == 'prereqs':
                        print("\n\r----[ PREREQ Array ]----\r\n\t")
                        print("{}\n\r").format(crse_dtl['prereqs'])
                        for parts in attrib:
                            if parts == 'courses':
                                print("\n\r----[ PREREQ Courses ]----\r\n\t")
                                print("{}\n\r").format(attrib['courses'])
                            if parts == 'coreqs':
                                print("\n\r----[ Co-Req Courses ]----\r\n\t")
                                print("{}\n\r").format(attrib['core'])

                # this_course_detail = ast.literal_eval(crse_dtl)
                # print this_course_detail
                # if crse_dtl['prereqs']:
                #     return_data = crse_dtl['prereqs']

    return return_data


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
        self.subjlist = list_of_subjects
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
