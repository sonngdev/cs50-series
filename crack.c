#define CHARNUM 52              // passwords use permutes of 52 chars in total
#define _XOPEN_SOURCE
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <unistd.h>

int main(int argc, string argv[])
{
    if (argc != 2)              // WRONG USAGE
    {
        printf("Usage: ./crack <hash>\n");
        return 1;
    }

    string hash = argv[1];      // RIGHT USAGE
    char salt[3];
    strncpy(salt, hash, 2);
    salt[2] = '\0';                     // hash & salt (first 2 chars of hash)

    char charArr[CHARNUM];
    for (int i = 0, j = 122; i < CHARNUM; i++, j--)
    {
        if (j == 96)
        {
            j = 90;
        }
        charArr[i] = (char) j;
    }                                   // initialize array of 52 chars

    for (int n = 1; n < 6; n++)         // brute force: try all one-, two-, ... char passwords
    {
        int count[n];                       // array of int to generate string
        char pw[n + 1];                     // one extra byte for null terminator
        for (int i = 0; i < n; i++)
        {
            count[i] = 0;                   // [ , ] -> [0, 0]
            pw[i] = charArr[0];             // [0, 0] -> "AA"
        }
        pw[n] = '\0';                       // "AA\0"
        int countSum = 0;                   // check if [51, 51] is reached

        while (strcmp(crypt(pw, salt), hash) != 0 && countSum < 51 * n)
        {
            count[0]++;                     // while haven't found pw
            countSum = 0;
            for (int i = 0; i < n; i++)         // check for overflowing like [52, 0]
            {
                if (count[i] > 51)
                {
                    if (i < n - 1)
                    {
                        count[i + 1]++;
                        count[i] = 0;
                    }
                }

                pw[i] = charArr[count[i]];      // generate new string
                countSum += count[i];
            }                                   // NOTES: does not check [51, 51]
        }

        if (strcmp(crypt(pw, salt), hash) == 0)
        {
            printf("Password is: %s\n", pw);
            return 0;
        }                                   // check [51, 51], or if pw has been found
    }
}