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

    for item in choices: #ndex, (key, value) in enumerate(choices.items):
        print item, choices[item]
        # for i in enumerate(item):
        #     print i

print "Imported file successfully. That is all"
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