#!/usr/bin/env python


import json  # data format
import urllib2  # fetch from API url
import re  # regular expressions
import logging

console = logging.getLogger("degree-map")


def ingest(io, a):  # json io, argprse object

    rtrn_str = ""
    # rtrn_str = ""  # return output
    crse_meta = {
        'course': None, 'type': None, 'credits': None,
        'college': None, 'xlist': None, 'colleges': []}
    crse_dtl = {
        'alpha': None, 'number': None, 'title': None,
        'desc': None, 'pre': None, 'prereqs': []}
    subjects = {}  # dictionary
    manifest = {}  # dict
    crse_lst = []  # list / array
    subj_lst = []  # list / array
    n = 0
    slot = 0  # iterators

    for i in io:
        # print i, io[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            crse_meta['course'] = str(io[i][-9:].strip())
            prts = crse_meta['course'].split("_")
            subjects[n] = [prts[1]]
            crse = "{} {}".format(prts[0], prts[1])
            subj = "{}".format(prts[0])
            crse_dtl['number'] = str(prts[1])
            crse_dtl['alpha'] = str(prts[0])
            crse_lst.append(crse)
            subj_lst.append(subj)
            details = get_course(crse_meta['course'])
            description = str(details['description'])
            # need to have '_' seperator when querying API
            course_title = str(details['course_title'])
            if (len(details['credits']) > 1):
                crse_crdts = int(details['credits'])
            else:
                crse_crdts = str(details['credits'])
            rtrn_str += "\n\r[[[Slot {}]]]\n\r [ Course: ]"
            rtrn_str += "\n\r\t{}: {} [{}]".format(
                slot, crse, course_title, crse_crdts)
            colleges = str(details['college'])
            crse_meta['college'] = colleges
            crse_meta['colleges'] = colleges.split("/")
            if a.verbose:
                for college in crse_meta['colleges']:
                    rtrn_str += "College: {}\n".format(college)
                    console
            if 'Pre:' in description:
                prts = description.split(" Pre: ")
                crse_dtl['desc'] = prts[0]
                if prts[1]:
                    crse_dtl['pre'] = prts[1]
                    if '(Same as ' in prts[1]:
                        crse_dtl['pre'] = prts[0]
                        xlistprts = prts[1].split("Same as ")
                        cleaned = xlistprts[1].split(")")
                        rtrn_str += "X-listed with {}\n".format(cleaned[0])
                        prereq = xlistprts[0].split("(")
                        crse_dtl['pre'] = prereq[0].strip()
                        # remove cross list from prerequisite text
                    hits = re.search(
                        '([A-Z]{2-4})(?:\w?(\d{3}[A-Z]?))+', crse_dtl['pre'])
                    # this is the regex serch .  Its failing.  Why?
                    if hits:
                        rtrn_str += ("\n\r----PREREQS: {}----\n\r\n\r").format(
                            hits.group())
                else:
                    rtrn_str += "No Prereqs!"
                    crse_dtl['desc'] = description
                    crse_dtl['pre'] = False

            if '(Attributes:' in description:
                prts = description.split("(Attributes: ")
                if crse_dtl['pre']:  # if pre has attributes in it, clean it up
                    pre = crse_dtl['pre'].split("(Attributes: ")
                    crse_dtl['pre'] = pre[0].strip()
                if prts[1]:
                    rtrn_str += "[ Attributes: ]\n\r\t"
                    attrib = prts[1].split(")")
                    attr = attrib[0].split(", ")
                    for attrib in attr:
                        rtrn_str += "{}\t".format(attrib)
                crse_dtl['desc'] = prts[0]

            # after processing API data, fetch prereqs from alternate manifest
            if crse_dtl['pre']:
                crse_chain = get_prereq(crse_dtl['alpha'], crse_dtl['number'])
                if a.broken:
                    if crse_chain:
                        rtrn_str += crse_chain

            if a.titles:
                rtrn_str += "[ Description: ]\n\r {}".format(crse_dtl['desc'])

            if crse_dtl['pre']:
                pretext = crse_dtl['pre'].split(",")
                for p, pretxt in enumerate(pretext):
                    rtrn_str += "Prereq #{} is: {}\n\r".format(p, pretxt)
                # rtrn_str += "[ Prereq: ]\n\r\t {}\n".format(crse_dtl['pre'])

            crse_dtl['title'] = course_title

            contact_type = str(details['contact_type'])

            if a.debug:
                rtrn_str += "{}  - [course] \n\r ".format(details)

            # if a.broken:
            #     subj_catalog = fetch(subj)
            #     rtrn_str += "Prepre for it.... \n\r {}".format(subj_catalog)

            # do some tuple packing!
            tag = (subj, crse, crse_crdts)
            meta = (contact_type, colleges)
            detail = (course_title, description)
            manifest[crse] = (tag, detail, meta)

            if a.debug:
                rtrn_str += manifest
                rtrn_str += tag

        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                crse_meta['course'] = str(io[i][-9:].strip())
                prts = crse_meta['course'].split("_")
                subjects[n] = [prts[1]]
                course = "{} {}".format(prts[0], prts[1])
                subj = "{}".format(prts[0])
                crse_dtl['number'] = str(prts[1])
                crse_dtl['alpha'] = str(prts[0])
                crse_lst.append(course)
                subj_lst.append(subj)
                details = get_course(crse_meta['course'])
                description = str(details['description'])
                # need to have '_' seperator when querying API
                course_title = str(details['course_title'])
                if (len(details['credits']) > 1):
                    crse_crdts = int(details['credits'])
                else:
                    crse_crdts = str(details['credits'])
                rtrn_str += "\n\r[ Slot {} ]\n\r [ {} ]:\n\r\t {} [{}]".format(
                    slot, course, course_title, crse_crdts)

                colleges = str(details['college'])
                crse_meta['college'] = colleges
                crse_meta['colleges'] = colleges.split("/")
                if a.verbose:
                    for college in crse_meta['colleges']:
                        rtrn_str += "College: {}\n".format(college)

                if 'Pre:' in description:
                    prts = description.split(" Pre: ")
                    crse_dtl['desc'] = prts[0]
                    if prts[1]:
                        crse_dtl['pre'] = prts[1]
                        if '(Same as ' in prts[1]:
                            crse_dtl['pre'] = prts[0]
                            xlistprts = prts[1].split("Same as ")
                            cleaned = xlistprts[1].split(")")
                            rtrn_str += "X-listed with {}\n".format(cleaned[0])
                            prereq = xlistprts[0].split("(")
                            crse_dtl['pre'] = prereq[0].strip()
                            # remove cross list from prerequisite text
                    else:
                        rtrn_str += "No Prereqs!"
                        crse_dtl['desc'] = description
                        crse_dtl['pre'] = False

                if '(Attributes:' in description:
                    prts = description.split("(Attributes: ")
                    if crse_dtl['pre']:  # if pre has attributes, clean it.
                        pre = crse_dtl['pre'].split("(Attributes: ")
                        crse_dtl['pre'] = pre[0].strip()
                    if prts[1]:
                        rtrn_str += "[ Attributes: ]\n\r\t"
                        attrib = prts[1].split(")")
                        attr = attrib[0].split(", ")
                        for attrib in attr:
                            rtrn_str += "{}\t".format(attrib)
                    crse_dtl['desc'] = prts[0]

                # process API data, then fetch prereqs from alternate manifest
                if crse_dtl['pre']:
                    crse_chain = get_prereq(
                        crse_dtl['alpha'], crse_dtl['number'])
                    if a.broken:
                        if crse_chain:
                            rtrn_str += crse_chain

                if a.titles:
                    rtrn_str += "[ Description: ] \n\r\t "
                    rtrn_str += "{}".format(crse_dtl['desc'])

                if crse_dtl['pre']:
                    pretext = crse_dtl['pre'].split(",")
                    for p, pretxt in enumerate(pretext):
                        rtrn_str += "API Pre: #{} is: {}\n\r".format(p, pretxt)
                    # rtrn_str += "[ Pre: ]\n\r\t {}\n".format(crse_dtl['pre'])

                crse_dtl['title'] = course_title

                # alpha = str(details['alpha'])
                contact_type = str(details['contact_type'])

                if a.debug:
                    rtrn_str += "{}  - [course] \n\r ".format(details)

                # do some tuple packing!
                tag = (subj, course, crse_crdts)
                meta = (contact_type, colleges)

                detail = (course_title, description)
                manifest[course] = (tag, detail, meta)

                if a.debug:
                    rtrn_str += manifest
                    rtrn_str += tag

    return rtrn_str

    def debug(loggername):
        logger = logging.getLogger(loggername)

        def log_(enter_message, exit_message=None):
            def wrapper(f):
                def wrapped(*args, **kargs):
                    logger.debug(enter_message)
                    r = f(*args, **kargs)
                    if exit_message:
                        logger.debug(exit_message)
                    return r
                return wrapped
            return wrapper
        return log_

# my_debug = debug('my.logger')

# @my_debug('enter foo', 'exit foo')
# def foo(a,b):
#     return a+b


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
    rtrn_data = False
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
                #     rtrn_data = crse_dtl['prereqs']

    return rtrn_data


def fetch(alpha):  # returns object
    subjurl = "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(alpha)
    # Parse JSON into an object with attributes corresponding to dict keys.
    response = urllib2.urlopen(subjurl)
    data = json.loads(response)
    # choices = json.loads(contents)
    # data = json.loads(data, object_hook=lambda d: namedtuple
    # course', d.keys())(*d.values()))
    return data
