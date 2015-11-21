#!/usr/bin/env python

import sys
import json
import argparse

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
            string = " %s - %s; " % (parts[0], parts[1])
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

    s = ''.join(l)
    print s

    print "There are %d slots with courses specified" % slot
    print "A total of %d courses were chosen" % len(courses)

    # print subjects.items
    for k, v in subjects.iteritems():
        print k, v

    print subjects.keys() # will give you all keys in list
    print subjects.values() # will give you values in list
    print subjects.items()  # will give you pair tuple of key and value
    # for i in courses:
    #     print courses[i]

    # for i in subjects:
    #     print subjects[i]

    # Read through entries, determine if they are courses
    # for item in catalog['courses']:
    #     courses
    #     if item['type'] == 'message' and '?' in item['text']:
    #         # Update dict
    #         user = item['user']
    #         if user in questions:
    #             questions[user] += 1
    #         else:
    #             questions[user] = 1

    # # Turn that dict into a list of (user, question_count) tuples
    # q_list = []
    # for user, count in questions.items():
    #     q_list.append( (user, count) )

    # # Sort the list
    # q_list = sorted(q_list, key = lambda x: x[1], reverse=True)

    # # Print results
    # print(q_list)

def isset(variable):
    return variable in locals() or variable in globals()

##########################

if __name__ == '__main__':
    main()