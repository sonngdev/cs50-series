from cs50 import get_string

# prompt user for card number
number = get_string("Number: ")

checksum = 0
index = 0

# number length is even or not
evenlength = len(number) % 2 == 0

# go through every digit
for c in number:

    # casting
    d = int(c)

    # multiply every other digit
    # even length
    if evenlength and index % 2 == 0:
        d *= 2

    # odd length
    elif not evenlength and index % 2 != 0:
        d *= 2

    # deal with number bigger than 9
    if d > 9:
        d = d // 10 + d % 10

    # update checksum and index
    checksum += d
    index += 1

# checksum ends in 0
if checksum % 10 == 0:

    # AMEX
    if len(number) == 15 and int(number[:2]) in [34, 37]:
        print("AMEX")

    # MASTERCARD
    elif len(number) == 16 and int(number[:2]) in [51, 52, 53, 54, 55]:
        print("MASTERCARD")

    # VISA
    elif len(number) in [13, 16] and number[0] == "4":
        print("VISA")

    # INVALID
    else:
        print("INVALID")

# INVALID
else:
    print("INVALID")