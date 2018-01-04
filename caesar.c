#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)                                  // WRONG USAGE
    {
        printf("Usage: ./caesar <non-negative integer>\n");
        return 1;
    }

    int k = atoi(argv[1]) % 26;                     // RIGHT USAGE
    string plain = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0, len = strlen(plain); i < len; i++)      // loop through every char in the string
    {
        if (isalpha(plain[i]))                              // if char is a letter,
        {
            if (isupper(plain[i]))                              // check if it is capitalized
            {
                int c = ((((int) plain[i] - 65) + k) % 26) + 65;
                printf("%c", (char) c);
            }

            else                                                // or not
            {
                int c = ((((int) plain[i] - 97) + k) % 26) + 97;
                printf("%c", (char) c);
            }
        }

        else                                                // if char is not a letter
        {
            printf("%c", plain[i]);
        }
    }

    printf("\n");
}