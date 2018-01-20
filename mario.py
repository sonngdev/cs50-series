from cs50 import get_int

# prompt for a non-negative, less-than-23 integer height
while True:
    n = get_int("Height: ")
    if n >= 0 and n <= 23:
        break

# printing
for i in range(n):

    # print spaces
    for j in range(n - (i + 1)):
        print(" ", end="")

    # print blocks
    for k in range(i + 1):
        print("#", end="")

    # print gap in between
    print("  ", end="")

    # print blocks
    for l in range(i + 1):
        print("#", end="")

    # new line
    print()