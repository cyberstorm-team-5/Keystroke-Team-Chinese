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

from multiprocessing import Process, Pool

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
keyPress = timings[:len(timings)/2 +1]
keyInterval = timings[len(timings)/2 +1:]

if(DEBUG):
        print "key press times = {}".format(keyPress)
        print "key intervals = {}".format(keyInterval)


#make list of start times for each key to be pressed (first one starts at time 0)
startTimes = [0]
for i in range(1, len(password)):
        #to support multiprocessing, get the time at which each key would be pressed based on the
        #time that would be accumulated at this point + the time the previous key is held down
        #for + the time between the previous key being released and the next being clicked (this
        #value could be negative if the next key were pressed before the previous was released)
        startTimes.append(startTimes[i-1] + keyPress[i-1] + keyInterval[i-1])


if(DEBUG):
        print "key start times = {}".format(startTimes)


#keyboard = Controller()


#keyData given as [key, startTime, holdTime] list
def typeKey(keyData):
        #setup keyboard seperately for each instance of this function to prevent collusion
        #between the different processes running concurrently
        keyboard = Controller()

        #sleep until start time is reached for the key, then press it
        sleep(keyData[1])
        keyboard.press(keyData[0])

        #these debugs show the time at which the key is pressed and released, respecitvely, to see if it
        #is all working as intended
        if(DEBUG):
                print time()
                
        #wait out the hold tiem before releasing the key
        sleep(keyData[2])
        keyboard.release(keyData[0])

        if(DEBUG):
                print time()

#make a tuple such that each value in the tuple is an array with three elements to be
#called with the typeKey function
keyData = ()
for i in range(len(password)):
        keyData += ([password[i], startTimes[i], keyPress[i]],)

if(DEBUG):
        print(keyData)


#setup multiprocessing pool using the keyData tuple such that the typeKey function is called
#numKeys times at once (where numKeys is the number of keys to be pressed for the password, so
#once instance of the function per key in the password). The reason for doing this async is to
#account for the case in which a key is pressed and then another key is aso pressed before the first
#one is released
def poolHandler(numKeys):
        p = Pool(numKeys)
        p.map(typeKey, keyData)

#initialize the asynchronous flow with multiprocessing only once (through main)
if __name__ == '__main__':
        poolHandler(len(password))





######################################OLD ATTEMPTS###################################################

#first attempt at multiprocessing (DOES NOT WORK)
def ogMultattempt():
        processList = []
        for i in range(len(password)):
                proc = Process(target=typeKey, args=(password[i], startTimes[i], keyPress[i]))
                processList.append(proc)
                proc.start()
                #typeKey(password[i], startTimes[i], keyPress[i])

        for proc in processList:
                proc.join()


#original code that does not take into account negative numbers for intervals, but assuming
#no negatives are present it works fine
def originalCode():
        #type each character in the string, where the time each key is held down for
        #and the interval of time for moving b/t keys is specified
        for i in range(0, len(password)):
                keyboard.press(password[i])
                #hold down key for time of keypress
                sleep(keyPress[i])
                keyboard.release(password[i])
                #no key interval wait time after the last key
                if(i != len(password) -1):
                        sleep(keyInterval[i])

        #flush out all of standard input (which will be teh specified string
        tcflush(stdout, TCIFLUSH)
        print









