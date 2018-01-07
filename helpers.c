// Helper functions for music

#include <cs50.h>
#include <string.h>
#include <math.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    string X = strtok(fraction, "/");
    string Y = strtok(NULL, "/");

    return 8 * atoi(X) / atoi(Y);
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    // Note name
    int name;
    switch (note[0])
    {
        case 'C':
            name = -9;
            break;
        case 'D':
            name = -7;
            break;
        case 'E':
            name = -5;
            break;
        case 'F':
            name = -4;
            break;
        case 'G':
            name = -2;
            break;
        case 'A':
            name = 0;
            break;
        case 'B':
            name = 2;
            break;
    }

    // Note accidental
    int accidental = 0;
    if (strlen(note) == 3)
    {
        switch (note[1])
        {
            case '#':
                accidental = 1;
                break;
            case 'b':
                accidental = -1;
                break;
        }
    }

    // 1 octave = 12 semitones
    // from the fourth octave
    int last = strlen(note) - 1;
    int octave = ((note[last] - '0') - 4) * 12;

    // Calculate semitones
    int semitones = name + accidental + octave;

    // Frequency = 2^(semitones/12) * 440
    return (int) round(pow(2, (double) semitones / 12) * 440);
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    return strcmp(s, "") == 0;
}
