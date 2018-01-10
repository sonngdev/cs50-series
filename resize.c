// Resizes a BMP file
// ALL CAPS INDICATES CHANGE FROM ORIGINAL CODE IN "COPY.C"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize <factor> <input_file> <output_file>\n");
        return 1;
    }

    // RESIZE FACTOR
    double f = atof(argv[1]);

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determining padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // MAKE NEW HEADERS
    BITMAPFILEHEADER bfnew;
    memcpy(&bfnew, &bf, sizeof(BITMAPFILEHEADER));
    BITMAPINFOHEADER binew;
    memcpy(&binew, &bi, sizeof(BITMAPINFOHEADER));

    // NEW DIMENSIONS
    binew.biWidth = (long) (binew.biWidth * f);
    binew.biHeight = (long) (binew.biHeight * f);

    // NEW PADDING
    int paddingnew = (4 - (binew.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // NEW IMAGE SIZE AND FILE SIZE
    binew.biSizeImage = ((sizeof(RGBTRIPLE) * binew.biWidth) + paddingnew) * abs(binew.biHeight);
    bfnew.bfSize = binew.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfnew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&binew, sizeof(BITMAPINFOHEADER), 1, outptr);

    // BIGGER
    if (f >= 1)
    {
        // CASTING
        int fi = (int) f;

        // iterate over infile's scanlines
        for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
        {
            // FOR FI TIMES
            for (int j = 0; j < fi; j++)
            {
                // iterate over pixels in scanline
                for (int k = 0; k < bi.biWidth; k++)
                {
                    // temporary storage
                    RGBTRIPLE triple;

                    // read RGB triple from infile
                    fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                    // FOR FI TIMES
                    for (int l = 0; l < fi; l++)
                    {
                        // write RGB triple to outfile
                        fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                    }
                }

                // skip over padding, if any
                fseek(inptr, padding, SEEK_CUR);

                // then add it back (to demonstrate how)
                for (int m = 0; m < paddingnew; m++)
                {
                    fputc(0x00, outptr);
                }

                // RESET CURSOR
                if (j != fi - 1)
                {
                    fseek(inptr, -(bi.biWidth * (bi.biBitCount / 8) + padding), SEEK_CUR);
                }
            }
        }
    }

    // SMALLER
    else if (f < 1)
    {
        // CASTING
        int fr = (int) (1 / f);

        // iterate over infile's scanlines
        for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight / fr; i++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth / fr; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // write RGB triple to outfile
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);

                // MOVE CURSOR
                fseek(inptr, (bi.biBitCount / 8) * (fr - 1), SEEK_CUR);
            }

            // skip over padding, if any
            fseek(inptr, padding, SEEK_CUR);

            // then add it back (to demonstrate how)
            for (int k = 0; k < paddingnew; k++)
            {
                fputc(0x00, outptr);
            }

            if (i != biHeight / fr - 1)
            {
                // SKIP LINES IN INFILE
                fseek(inptr, (bi.biWidth * (bi.biBitCount / 8) + padding) * (fr - 1), SEEK_CUR);
            }
        }
    }


    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
