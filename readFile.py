#! usr/bin/python/

from sys import argv
from os.path import exists


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

script, from_file = argv

print "Reading from %s" % (from_file)

#we could do these two on one line, how?
in_file = open(from_file)
indata = in_file.read()

print "The input file is %d bytes long" % len(indata)

char_count = 0
for char in indata:
#	print "line is : %s" % (line)
	char_count +=1

# char_count = sum(1 for line in in_file)

# char_count = sum(1 for line in open(in_file))

print "There are %d characters in the file." % (char_count)
print "The length of the file is %d lines" % (file_len(from_file))
in_file.close()
