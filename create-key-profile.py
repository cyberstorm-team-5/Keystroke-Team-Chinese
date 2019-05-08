#this code creates a keystroke profile to use with faketyping.py
#RUN: python2.7 create-key-profile.py < password > file.txt

password = raw_input()

passOut = ""

for char in password:
        passOut += char + ","

for i in range(len(password)-1):
        passOut += password[i] + password[i+1] + ","



print passOut[:-1]
