# Questions

## What's `stdint.h`?

A library for BMP-related data types based on Microsoft's.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

`uint8_t` is used for 8-bit unsigned integers (ranging from 0 to 255).
`uint32_t` is used for 32-bit unsigned integers (ranging from 0 to 4,294,967,295).
`int32_t` is used for 32-bit signed integers (ranging from -2,147,483,647 to 2,147,483,647).
`uint16_t` is used for 16-bit unsigned integers (ranging from 0 to 65,535).

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

A `BYTE` is 1 byte big (8 bits).
A `DWORD` is 4 bytes big (32 bits).
A `LONG` is 4 bytes big (32 bits).
A `WORD` is 2 bytes big (16 bits).

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

In ASCII: B,M
In decimal: 66, 77
In hexadecimal: 0x42, 0x4D

## What's the difference between `bfSize` and `biSize`?

`bfSize` indicates the size, in bytes, of the bitmap file.
`biSize` is the number of bytes required by the structure.

## What does it mean if `biHeight` is negative?

If `biHeight` is negative, the bitmap is a top-down DIB and its origin is the upper-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

`biBitCount` specifies BMP's color depth.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

`fopen` might return `NULL` if the file that is being opened to read does not exist.

## Why is the third argument to `fread` always `1` in our code?

Because there is only one File Header and one Info Header for each file.

## What value does line 65 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

`padding` is `3`.

## What does `fseek` do?

`fseek` keeps track of where in the file we are. In copy.c, we need to call it to update
the cursor everytime we need to skip the padding.

## What is `SEEK_CUR`?

The current position in the file of the cursor.
