#!/usr/bin/env python

import sys
import json
import argparse
from collections import Counter 
#ht/ http://stackoverflow.com/questions/2600191/

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

    for item in choices: 
        print item, choices[item]
        if (item[:9] == 'dgre-slot'):
            slot += 1
            courses[slot] = choices[item][-9:].strip()
            parts = courses[slot].split("_")
            subjects[slot] = parts[0]
            # make a tuple foreacch subject, store required courses

        elif (item[:8] == 'req_slot'):
            slot += 1
            courses[slot] = choices[item][-9:].strip()
            parts = courses[slot].split("_")
            subjects[slot] = parts[0]
        elif (item[:5] == 'slot-'):
            if (item[6:7] == ' '):
                slot += 1
                courses[slot] = choices[item][-9:].strip()
                parts = courses[slot].split("_")
                subjects[slot] = parts[0]
        # for i in enumerate(item):
        #     print i

    print "There are %d slots with courses specified" % slot
    print "A total of %d courses were chosen" % len(courses)

    instances = Counter(subjects)
    # print instances.count("MATH")
    print Counter(subjects).most_common()

    for i in courses:
        print courses[i]

    # for i in subjects:
    #     print subjects[i]
# Create a dictionary that maps subjects, courses



    # subject courses = {}

#for line in file ? 
#for json parse args 
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


##########################

if __name__ == '__main__':
    main()