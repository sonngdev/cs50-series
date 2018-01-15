# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

Pneumonoultramicroscopicsilicovolcanoconiosis means a lung disease caused by inhaling very fine ash and sand dust.

## According to its man page, what does `getrusage` do?

`getrusage` is a function that returns resource usage statistics for the calling process, which is the sum of resources used by all threads in the process.

## Per that same man page, how many members are in a variable of type `struct rusage`?

There are 16 members in a variable of type `struct rusage`.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Instead of making copies of `before` and `after` when we pass them by value, we can just pass them by reference so no unnecessary variables are created, thus save space.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

Every word in a file is checked, character by character.
As long as the character we are checking is alphabetical or a apostrophe (the apostrophe must not lie at the beginning of a word), we update the word array and the index counter.
If the index counter exceeds the maximum length of a word, i.e. a word is too long, we dispose of the excess characters.
When we see a number, immediately get rid of the whole word, reset the index counter and move on to a new word.
When we reach a space, that means a word is found. We terminate the word with `'\0'`, update word counter, and update total check time.
If the word is misspelled, we update misspelled word counter and print the word.
Lastly, we reset the index counter to zero to prepare to check for the next word.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

We don't know how long a word can get, so using `fscanf` can lead to a buffer overflow which crashes the program. With `fgetc` we can dispose of the remaining characters of a word should it get too long.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

As we are passing pointers to strings to `load` and `const`, i.e. passing by reference, we may accidentally modify the actual value of those strings,
thus break our code. `const` is meant to prevent this, since parameters declared with `const` cannot be changed.
