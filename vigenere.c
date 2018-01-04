#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

bool allalpha(string s);

int main(int argc, string argv[])
{
    if (argc != 2 || !allalpha(argv[1]))                // WRONG USAGE
    {
        printf("Usage: ./caesar <alphabetical keyword>\n");
        return 1;
    }

    string keystr = argv[1];                            // RIGHT USAGE
    int keylen = strlen(keystr), keyarr[keylen];
    for (int i = 0; i < keylen; i++)                            // array of keys from the keyword
    {
        if (isupper(keystr[i]))
        {
            keyarr[i] = (int) keystr[i] - 65;
        }

        else
        {
            keyarr[i] = (int) keystr[i] - 97;
        }
    }

    string plainstr = get_string("plaintext: ");
    printf("ciphertext: ");

    int count = 0;                                              // count is the next key used
    for (int i = 0, plainlen = strlen(plainstr); i < plainlen; i++)
    {
        char c = plainstr[i];
        if (isalpha(c))                                         // if char is a letter,
        {
            if (isupper(c))                                         // check if it is capitalized
            {
                int cipher = ((((int) c - 65) + keyarr[count]) % 26) + 65;
                printf("%c", (char) cipher);
            }

            else                                                    // or not
            {
                int cipher = ((((int) c - 97) + keyarr[count]) % 26) + 97;
                printf("%c", (char) cipher);
            }

            count++;
            if (count == keylen)                                // reset "count" if no next key exists
            {
                count = 0;
            }
        }

        else                                        // if char is not a letter, print and do not increase "count"
        {
            printf("%c", plainstr[i]);
        }
    }

    printf("\n");
}

bool allalpha(string s)                 // check whether all chars in a string is alphabetical
{
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (!isalpha(s[i]))
        {
            return false;
        }
    }
    return true;
}