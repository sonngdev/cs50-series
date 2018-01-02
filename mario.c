#include <cs50.h>
#include <stdio.h>

void makePyramid(int n);
void indent(int n);
void block(int n);


int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 0 || n > 23);
    makePyramid(n);
}

void makePyramid(int n)
{
    for (int i = 0; i < n; i++)
    {
        indent(n - i - 1);
        block(i + 1);
        printf("  ");
        block(i + 1);
        printf("\n");
    }
}

void indent(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf(" ");
    }
}

void block(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
}