import crypt
import sys

# wrong usage
if len(sys.argv) != 2:
    print("Usage: python crack.py [hash]")
    sys.exit(1)

# hash & salt
h = sys.argv[1]
s = h[:2]

# init char list
CHARNUM = 52
charArr = []
ch = 122
for i in range(CHARNUM):
    charArr.append(chr(ch))
    ch -= 1
    if ch == 96:
        ch = 90

# try every length from 1 to 5 chars
for length in range(1, 6):

    # count list and password
    count = []
    pw = ""

    # initial password
    for i in range(length):
        count.append(0)
        pw += charArr[count[i]]

    # while pw not found and last pw for this length not reached
    while (crypt.crypt(pw, s) != h and not all(x == 51 for x in count)):

        # try next char
        count[0] += 1

        # reset pw
        pw = ""

        for i in range(length):

            # roll-over
            if count[i] > 51:
                if i < length - 1:
                    count[i + 1] += 1
                    count[i] = 0

            # append new char to pw
            pw += charArr[count[i]]

    # pw is found
    if crypt.crypt(pw, s) == h:
        print("Password is: " + pw)
        sys.exit(0)