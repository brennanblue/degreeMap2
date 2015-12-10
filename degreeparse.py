#!/usr/bin/env python


import json  # data format
import urllib2  # fetch from API url
# import re  # regular expressions
import logging
# from manifest import Choices

console = logging.getLogger("degree-map")


def ingest(io, a, data=False):  # json io, argprse object
    # rtrn_data = {}
    rtrn_str = ""
    # rtrn_str = ""  # return output
    # subjects = {}
    manifest = {}  # dict
    # crse_lst = []  # list / array
    # subj_lst = []  # list / array
    # n = 0
    slot = 0  # iterators

    for i in io:
        # print i, io[i]
        if (i[:9] == 'dgre-slot' or i[:8] == 'req_slot'):
            slot += 1
            choice = str(io[i][-9:].strip())  # alpha+'_'+num
            crse_meta = populate_course_meta(choice)
            crse_dtl = populate_course_detail(choice)  # redundant?
            # subjects[n] = subj
            # crse_lst.append(crse)
            # subj_lst.append(subj)
            # after processing API data, fetch prereqs from alternate manifest

        elif (i[:5] == 'slot-'):
            if (i[6:7] == ' '):
                slot += 1
                choice = str(io[i][-9:].strip())
                crse_meta = populate_course_meta(choice)
                crse_dtl = populate_course_detail(choice)  # redundant?
                print("{}\n\r{}".format(crse_dtl, crse_meta))

    if data:
        print "There were {} slots with courses specified".format(slot)
        return manifest
    else:
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


def get_course(crse):  # returns course detail
    rtrn_data = False
    if ' ' in crse:
        prts = crse.split(" ")
        crse = "{}_{}".format(prts[0], prts[1])
    url = "http://hilo.hawaii.edu/courses/api/1.1/course/{}".format(crse)
    print url
    response = urllib2.urlopen(url)
    if response:
        data = json.load(response)
        if data:
            rtrn_data = data[0]
    return rtrn_data


def populate_course_meta(crse):  # returns dictionary of tuples
    rtrn_str = ""  # not used, but could be w/ flag
    crse_meta = {
        'course': None, 'type': None, 'credits': None, 'attrib': [],
        'college': None, 'colleges': [], 'xlist': []}  # , 'pre': []}
    # subjects = {}  # dictionary
    if '_' in crse:
        prts = crse.split("_")
    elif ' ' in crse:
        prts = crse.split(" ")
        crse = "{}_{}".format(prts[0], prts[1])
    else:
        print "Odd input doesn't conform"
    crse_meta['course'] = crse  # backup for checking
    print "Checking course Meta: {}".format(crse)
    details = get_course(crse)
    # crse_meta['type'] = details['contact_type']  # unicode?
    if (details['credits']):
        crse_crdts = str(details['credits'])
    else:
        crse_crdts = int(details['credits'])
    rtrn_str += "\n\r{}:[{}]\n\r".format(crse, crse_crdts)  # unused
    if '(Attributes:' in details['description']:
        prts = details['description'].split("(Attributes: ")
        if prts[1]:
            rtrn_str += "[ Attributes: ]\n\r"  # unused
            attrib = prts[1].split(")")
            attr = attrib[0].split(", ")
            for attrb in attr:
                rtrn_str += "{}\t".format(attrb)  # unused
                crse_meta['attrib'] = rtrn_str
    colleges = str(details['college'])
    crse_meta['college'] = colleges
    crse_meta['colleges'] = colleges.split("/")
    # if a.verbose:
    for college in crse_meta['colleges']:
        rtrn_str += "College: {}\n".format(college)
    xlistprts = details['description'].split("Same as ")
    if len(xlistprts) > 1:
        xlist = xlistprts[1].split(")")
        rtrn_str += "X-listed with {}\n".format(xlist[0])
        if xlist[0]:
            for xlst in xlist[0]:
                crse_meta['xlist'].append(xlst)
    rtrn_str += "{}  - [course] \n\r ".format(details)
    return rtrn_str
    # if a.broken:
    # subj_catalog = fetch(subj)
    # rtrn_str += "Prepre for it.... \n\r {}".format(subj_catalog)


def populate_course_detail(crse):
    rtrn_str = ""  # unused for now
    crse_dtl = {  # fill in blanks / keyed dictionary
        'alpha': None, 'number': None, 'title': None,
        'desc': None, 'pre': None}  # , 'prereqs': [] to meta
    if '_' in crse:
        prts = crse.split("_")
    elif ' ' in crse:
        prts = crse.split(" ")
        crse = "{}_{}".format(prts[0], prts[1])
    else:
        print "Odd input doesn't conform"

    # crse = "{} {}".format(prts[0], prts[1])
    # subj = str(prts[0])
    crse_dtl['number'] = str(prts[1])
    crse_dtl['alpha'] = str(prts[0])
    print "Checking course detail : {}".format(crse)
    details = get_course(crse)  # API call
    if details:
        crse_dtl['desc'] = str(details['description'])
        crse_dtl['title'] = str(details['course_title'])
        # now onto the difficult part, parsing prereqs
        if 'Pre:' in crse_dtl['desc']:
            prts = crse_dtl['desc'].split(" Pre: ")
            crse_dtl['desc'] = prts[0]
            if prts[1]:
                crse_dtl['pre'] = prts[1]
                if '(Same as ' in prts[1]:
                    crse_dtl['pre'] = prts[0]
        else:
            rtrn_str += "No Prereqs!"
            crse_dtl['pre'] = False  # redundant?

    if crse_dtl['pre']:
        crse_chain = get_prereq(crse_dtl['alpha'], crse_dtl['number'])
        # if a.broken:
        if crse_chain:
            rtrn_str += crse_chain
        pretxt = crse_dtl['pre'].split(",")
        for p, prtxt in enumerate(pretxt):
            rtrn_str += " - Prereq #{} is: {}\n\r".format(p, prtxt)
        # rtrn_str += "[ Prereq: ]\n\r\t {}\n".format(crse_dtl['pre'])

    # if a.titles:
    rtrn_str += "Description:\n\r {}\n\r".format(crse_dtl['desc'])
    return crse_dtl


def get_prereq(alpha, number):  # returns course detail
    l = "http://webdev.uhh.hawaii.edu/timeline/courses/_{}.json".format(alpha)
    response = urllib2.urlopen(l)
    if response:
        data = json.load(response)
    # rtrn_data = False
    rtrn_str = ""
    if data['courses']:
        for crse_dtl in data['courses']:
            if crse_dtl['number'] == number:
                # print crse_dtl
                for attr in crse_dtl:
                    if attr == 'prereqs':
                        rtrn_str += "\n\r----[ PREREQ Array ]----\r\n\t"
                        rtrn_str += "{}\n\r".format(crse_dtl['prereqs'])
                        for parts in attr:
                            if parts == 'courses':
                                rtrn_str += "\n\r---[ Prereq Courses ]---\n\r"
                                rtrn_str += "\t{}\n\r".format(attr['courses'])
                            if parts == 'coreqs':
                                rtrn_str += "\n\r---[ Co-Req Courses ]---\n\r"
                                rtrn_str += "\t{}\n\r".format(attr['core'])

    return rtrn_str  # data


def fetch(alpha):  # returns object
    subjurl = "http://hilo.hawaii.edu/courses/api/1.1/subject/{}".format(alpha)
    # Parse JSON into an object with attributes corresponding to dict keys.
    response = urllib2.urlopen(subjurl)
    data = json.loads(response)
    # choices = json.loads(contents)
    # data = json.loads(data, object_hook=lambda d: namedtuple
    # course', d.keys())(*d.values()))
    return data
