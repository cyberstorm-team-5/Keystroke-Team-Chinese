from pynput.keyboard import Key, Controller
from time import time, sleep
from random import uniform
from termios import tcflush, TCIFLUSH
from sys import stdin, stdout

#the bound for the durations of how long a key is held before beign released
HOLD_LOWER = 0.02
HOLD_UPPER = 0.2

keyboard = Controller()

#this is the string which will be typed up in the way specified below
string = "This will be typed out now..."

#type each character in the string, where the time each key is held down for
#and the interval of time for moving b/t keys is specified
for char in string:
        keyboard.press(char)
        #hold down key for time in range [HOLD_LOWER, HOLD_UPPER]
        sleep((uniform(HOLD_LOWER, HOLD_UPPER)))
        keyboard.release(char)

#flush out all of standard input (which will be teh specified string
tcflush(stdin, TCIFLUSH)
print
