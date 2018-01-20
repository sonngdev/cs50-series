from cs50 import get_float

# ensure non-negative input
while True:
    fchange = get_float("Change owed: ")
    if fchange >= 0:
        break

# convert to cents to avoid float imprecision
ichange = int(round(fchange * 100))

# list of available coins
coins = [25, 10, 5, 1]

# coins owed count
count = 0

# index of coins array
i = 0

# loop through array of coins
while ichange != 0:

    # can use that coin
    if ichange >= coins[i]:

        # decrease change
        ichange -= coins[i]

        # increase coin count
        count += 1

    # can't use that coin
    else:

        # look at next coin
        i += 1

# output
print(count)