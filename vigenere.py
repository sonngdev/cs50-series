import sys

from cs50 import get_string

# wrong usage
if len(sys.argv) != 2 or not sys.argv[1].isalpha():
    print("Usage: python vigenere.py [key]")
    exit(1)

# make list of key
keylist = []
for c in sys.argv[1]:

    # uppercase char
    if c.isupper():
        keylist.append(ord(c) - 65)

    # lowercase char
    else:
        keylist.append(ord(c) - 97)

# prompt user for plain text
plain = get_string("plaintext: ")

# init cipher text and index
cipher = ""
index = 0

# loop through every char in plain text
for c in plain:

    # alphabetical char
    if c.isalpha():

        # uppercase letter
        if c.isupper():
            cipher += chr((ord(c) + keylist[index] - 65) % 26 + 65)

        # lowercase letter
        else:
            cipher += chr((ord(c) + keylist[index] - 97) % 26 + 97)

        # increase index, reset if it exceeds keylist length
        index += 1
        if index == len(keylist):
            index = 0

    # not alphabetical, keep the char
    else:
        cipher += c

# output the cipher text
print("ciphertext: " + cipher)
sys.exit(0)