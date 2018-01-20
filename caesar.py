import sys
from cs50 import get_string


# wrong usage
if len(sys.argv) != 2:
    print("Usage: python caesar.py [key]")
    sys.exit(1)

# key
k = int(sys.argv[1]) % 26

# get plain text from user
plain = get_string("plaintext: ")

# init cipher text
cipher = ""

# loop through every char
for c in plain:

    # alphabetical char
    if c.isalpha():

        # cipher uppercase char
        if c.isupper():
            cipher += chr(((ord(c) + k - 65) % 26) + 65)

        # cipher lowercase char
        else:
            cipher += chr(((ord(c) + k - 97) % 26) + 97)

    # non-alphabetical char
    else:

        # keep that char
        cipher += c

# print output
print("ciphertext: " + cipher)
sys.exit(0)
