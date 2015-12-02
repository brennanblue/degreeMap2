readme.txt

# instructions

##tl;dr##
1. go to http://webdev.uhh.hawaii.edu/timeline/index-autoload.php
2. **press buttons**
3. save output to 'myfile.whatever'
4. python degreemap.py myfile.whatver (*-t for course titles / description )
5. report or squash bugs at http://github.com/brennanblue/degreeMap2

##usage##

use the [buggy] javascript console to configure degree parameters (major, minor, core requirements). To transfer the course selections at this point, a box or radio button must be ticked. don't worry about multiple instances of a course. edge cases needed for testing, front-end logic needed to automate repetitive box-ticking. most menus are shrinkable, not all serialization to text boxes is complete (sequences, groups). 

Some degrees have '*groups*' - requirements to achieve some # of credits from a pool of courses) these may be subdivided into '*blocks*', where the pool of courses is the same, but the allowable choices are diminished - i.e. "Choose 12 credits from [ART 282, ART 384, CS 151, CS 321", BUS 200, BUS 326], 6 of which must be at 300 level or above." would translate into two 6 credit '*blocks*' from the '*group*' of qualifying courses.

Some degrees have problems; these may present themselves politely with an ajax error message from the failed load, or may just silently fail when rendering the degree requirements. Please just ignore these for right now. Bug reports welcomed at brennanv@hawaii.edu. 

> Note the instance of radio buttons and checkboxes; it signifies when an option is exclusive. This front-end detail has frustrated the javascript logic to automate the selection of parallel course instances (same course as a prereq for multiple others).  Some instances have a checkbox next to a course instance, some have it as a radio button - those with a checkbox can be safely 'ticked' massively, but changing the radio group is problematical.  *jquery problems* ... for another day.

Upon submit, the php / js / html form will print a *json* encoded string with serialized contents of POST array. Save this file to the working directory (wherever degreemap.py can be found) as **myfile.whatever**, and run the program thusly: 
> python degreemap.py **myfile.whatever** (*-t* toggles course descriptions)

all of the debug output consisting of course details retrieved from the UH Hilo courses API is printed to the screen, so it can take several seconds to retrieve and parse all of the data. expect several screens of data.  If you don't have a scrollbar on your terminal / command line window, you'll get one.

Rudimentary parsing of the API output is used to print details (x-list, prerequisites, attributes) which are not directly output from version 1.1 of the API. (*latest as of 12/15 The curious can investigate error-triggering courses by following instructions at at http://hilo.hawaii.edu/courses/api/1.1/help.txt

## development ## 

Right now, the prereq courses are contained in a string. This needs to become structured data in the same format / syntax as the course objects, so that all required courses are present in the final course manifest. Once this list is complete, the sorting and sifting can begin. 

Future development of the timeline will hinge upon parsing the prereq string into a list of identifiable courses, and connecting courses together to form *chains*, from 1 to **n** links long, where n is the furthest out course from the 1st semester. (In theory, no course chain should be more than 8 units long in a four year degree, since the links map out to semseter slots in academic years. )

Since every course (*for now, we'll make this assumption*) need only be taken once, at the beginning of processing, the selected courses can be reduced to a set (unique items only). With just one 'course' object for each unique course the collection will initially be wide and shallow - all chains with a depth of one. That collection should then be sorted into with / without prereqs. Iterating through the set of courses with prereqs, prereq slots will be assigned to courses recursively, removing course objects from the pool as they are incorporated into longer 'chains'. The expected result of this process is approximately 40 courses, organized into 10-20 chains of dependence.

The course sorting algorighm {to be developed} will prioritize these chains and start filling in semesters from the end of the degree.  Thus, expect a 400 level class with a 7 level chain of prerequisite courses to be given first priority in allocating choices for each scheduled semester. A single elective course with no prerequisites can be slotted in last, once all of the tricker chains have been placed. 