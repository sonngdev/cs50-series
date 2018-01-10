// Recover deleted JPEG images
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define NAMELENGTH 7

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover card.raw\n");
        return 1;
    }

    // remember original file name
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // count
    int count;

    // outfile name
    char *outfile = malloc(sizeof(char) * (NAMELENGTH + 1));
    outfile[7] = '\0';

    // outfile pointer
    FILE *outptr;

    // buffer
    BYTE buffer[512];

    // flag
    bool found = false;

    // fread() on EOF will return less than 512
    while (fread(&buffer, 1, 512, inptr) == 512)
    {
        // start of a JPEG file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // first JPEG we find
            if (found == false)
            {
                // set initial count
                count = 0;

                // turn on flag
                found = true;
            }

            // not first JPEG
            else
            {
                // close previous file
                fclose(outptr);

                // increase count
                count++;
            }

            // create file name
            sprintf(outfile, "%03i.jpg", count);
            // outfile[7] = '\0';

            // open new file to write
            outptr = fopen(outfile, "w");
            if (outptr == NULL)
            {
                fclose(inptr);
                fprintf(stderr, "Could not create %s.\n", outfile);
                return 3;
            }

            // write
            fwrite(&buffer, 1, 512, outptr);
        }

        // not a start of a JPEG file
        else
        {
            // ignore blocks that are not in JPEG files
            if (found == true)
            {
                fwrite(&buffer, 1, 512, outptr);
            }
        }
    }

    // close last outfile
    fclose(outptr);

    // close infile
    fclose(inptr);
}