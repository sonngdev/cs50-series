// Implements a dictionary's functionality

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#include "dictionary.h"

bool freeup(node* this_node);
bool isempty(node* this_node);

// root node
node* root;

// char in dictionary file
char ch;

// total word count in dictionary
int word_count;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open dictionary
    FILE* dict = fopen(dictionary, "r");

    // initialize root node
    root = malloc(sizeof(node));
    root->is_word = false;
    for (int i = 0; i < 27; i++)
    {
        root->children[i] = NULL;
    }

    // initialize word count
    word_count = 0;

    // dealing with root node first
    node* this_node = root;

    // get every char in dictionary
    for (ch = fgetc(dict); ch != EOF; ch = fgetc(dict))
    {
        // not the end of a word
        if (ch != '\n')
        {
            // determine which child node to go to
            int child_index = (ch >= 'a') ? (int) (ch - 'a') : 26;

            // child node not point to anything yet
            if (!this_node->children[child_index])
            {
                // create a new node
                node* new_node = malloc(sizeof(node));
                new_node->is_word = false;
                for (int i = 0; i < 27; i++)
                {
                    new_node->children[i] = NULL;
                }

                // child node point to that new node
                this_node->children[child_index] = new_node;
            }

            // go to that child node
            this_node = this_node->children[child_index];
        }

        // at the end of a word
        else
        {
            // confirm this is the end
            // point of a right word
            this_node->is_word = true;

            // increase word count
            word_count++;

            // return to root node, prepare to
            // create a new path for a new word
            this_node = root;
        }
    }

    // close dictionary
    fclose(dict);

    // loaded successfully or not
    return ch == EOF;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return (ch == EOF) ? word_count : 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // start from root node
    node* this_node = root;

    // check every char in word
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        // make lowercase
        char letter = tolower(word[i]);

        // determine which child node to go to
        int child_index = (letter >= 'a') ? (int) (letter - 'a') : 26;

        // child node not point to anything
        if (!this_node->children[child_index])
        {
            // then it is a misspelled word
            return false;
        }

        // child node point to another node
        else
        {
            // go to that node, continue checking
            this_node = this_node->children[child_index];
        }
    }

    // at the end of the word being checked,
    // see if it is a stop of any right word
    return this_node->is_word;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    return freeup(root);
}

// Recursive function that free up every child node in a node, and the node itself
// Return true if cleared up successfully, otherwise return false
bool freeup(node* this_node)
{
    // child node array is empty
    if (isempty(this_node))
    {
        // free up this node
        free(this_node);

        // clear up successfully
        return true;
    }

    // child node array is not empty
    else
    {
        // go through every child node
        for (int i = 0; i < 27; i++)
        {
            // if see an empty child node
            if (this_node->children[i])
            {
                // empty it
                bool freed = freeup(this_node->children[i]);

                // fail to clear up
                if (!freed)
                {
                    return false;
                }
            }
        }

        // then empty the whole node
        free(this_node);

        // clear up successfully
        return true;
    }
}

// Check if a node's child node array is empty
bool isempty(node* this_node)
{
    // go through child node array
    for (int i = 0; i < 27; i++)
    {
        // if see a child node not empty
        if (this_node->children[i])
        {
            return false;
        }
    }

    // all child nodes are empty
    return true;
}