from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    # string lengths
    lenA = len(a)
    lenB = len(b)

    # init cost matrix
    matrix = [[(0, None)]]
    for row in range(1, lenA + 1):
        matrix.append([(row, Operation.DELETED)])
    for col in range(1, lenB + 1):
        matrix[0].append((col, Operation.INSERTED))

    # each row
    for i in range(1, lenA + 1):

        # each column in row
        for j in range(1, lenB + 1):

            # deletion cost
            delete = (matrix[i - 1][j][0] + 1, Operation.DELETED)

            # insertion cost
            insert = (matrix[i][j - 1][0] + 1, Operation.INSERTED)

            # substitution cost
            if a[i - 1] == b[j - 1]:
                subs = (matrix[i - 1][j - 1][0], Operation.SUBSTITUTED)
            else:
                subs = (matrix[i - 1][j - 1][0] + 1, Operation.SUBSTITUTED)

            # cost[i][j] is min of the three
            li = sorted([delete, insert, subs], key=takeFirst)
            matrix[i].append(li[0])

    # done
    return matrix


# key function to sort
def takeFirst(e):
    return e[0]
