#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // ensure non-negative input
    float fchange;
    do
    {
        fchange = get_float("Change owed: ");
    }
    while (fchange < 0);

    // convert to cents to avoid float imprecision
    int ichange = (int) round(fchange * 100);

    // array of available coins
    int coins[] = {25, 10, 5, 1};

    // coins owed count
    int count = 0;

    // index of coins array
    int i = 0;

    // loop through array of coins
    while (ichange != 0)
    {
        // can use that coin
        if (ichange >= coins[i])
        {
            // decrease change
            ichange -= coins[i];

            // increase coin count
            count++;
        }

        // can't use that coin
        else
        {
            // look at next coin
            i++;
        }
    }

    // output
    printf("%i\n", count);
}