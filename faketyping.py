#######################################################################################################
# NAME: Team Chinese fake typing keystroke dynamics
# RUN: "python2.7 faketyping.py < fakeprofile.txt"
# ABOUT: take in file where first line is comma seperated letters in password, followed
#        by comma seperated transitions b/t characters (ex: for password "ate", have line
#        1 be "a,t,e,at,te") Line 2 will contain comma seperated key press times
#        followed by key interval times for the values on the line above
#######################################################################################################
#IMPORTS
from pynput.keyboard import Key, Controller
from time import time, sleep
from random import uniform
from termios import tcflush, TCIFLUSH
from sys import stdin, stdout

#GLOBALS
DEBUG = False


#############################################MAIN#########################################################

#take in two lines of the file
password = raw_input()
timings = raw_input()

if(DEBUG):
        print "password = {}".format(password)
        print "timings = {}".format(timings)

#get password ready from file (remove commas on line 1 and only use the non-interval parts
password = password.split(",")
password = password[:len(password)/2 +1]
password = "".join(password)

if(DEBUG):
        print password

#get timings arrays ready for both keypresses and intervals
timings = timings.split(",")
timings = [float(a) for a in timings]
keypress = timings[:len(timings)/2 +1]
keyinterval = timings[len(timings)/2 +1:]

if(DEBUG):
        print "key press times = {}".format(keypress)
        print "key intervals = {}".format(keyinterval)


keyboard = Controller()


#type each character in the string, where the time each key is held down for
#and the interval of time for moving b/t keys is specified
for i in range(0, len(password)):
        keyboard.press(password[i])
        #hold down key for time of keypress
        sleep(keypress[i])
        keyboard.release(password[i])
        #no key interval wait time after the last key
        if(i != len(password) -1):
                sleep(keyinterval[i])

#flush out all of standard input (which will be teh specified string
tcflush(stdout, TCIFLUSH)
print









