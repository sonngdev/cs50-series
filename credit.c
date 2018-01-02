#include <cs50.h>
#include <stdio.h>

string check(long long n);
long long expo(int n);

int main(void)
{
    long long n;
    do
    {
        n = get_long_long("Number: ");
    }
    while (n < 0);
    printf("%s\n", check(n));
    return 0;
}

string check(long long n)
{
    int sum = 0, i = 0;

    do                                          // Step 1: calculate sum
    {
        i++;
        int d = (n % expo(i)) / expo(i - 1);
        if (i % 2 == 0)
        {
            d *= 2;                                     // double every other digit
        }
        if (d > 9)
        {
            d = (d / 10) + (d % 10);                    // first digit + second digit
        }
        sum += d;
    }
    while (expo(i) < n);

    int a = (n % expo(i)) / expo(i - 1);        // Step 2: capture two first digits
    int b = (n % expo(i - 1)) / expo(i - 2);    //         i stops at the number of digits of n

    if (sum % 10 == 0)                          // Step 3: check: if sum ends in 0:
    {
        if (i == 15 && a == 3)                          // 15 digits and starts with 34 or 37
        {
            switch (b)
            {
                case 4:
                case 7:
                    return "AMEX";
                    break;
            }
        }
        if (i == 16 && a == 5)                          // 16 digits and starts with number from 51 to 55
        {
            switch (b)
            {
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                    return "MASTERCARD";
            }
        }
        if ((i == 13 || i == 16) && a == 4)             // 13 or 16 digits and starts with 4
        {
            return "VISA";
        }
    }
    return "INVALID";                       // default: invalid card
}

long long expo(int n)                       // function to calculate 10^n
{
    long long x = 1;
    for (int i = 0; i < n; i++)
    {
        x *= 10;
    }
    return x;
}