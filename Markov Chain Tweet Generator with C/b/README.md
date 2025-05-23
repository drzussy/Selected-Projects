# Generic Markov Chain Text Generator

This is a generic Markov Chain text generator program that reads input text and generates random sentences based on the statistical patterns it finds in the input data. It uses generic programming concepts in C to make it adaptable to various data types and can generate multiple random sentences.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Algorithm Overview](#algorithm-overview)
- [Code Structure](#code-structure)
- [Generic Programming](#generic-programming)

### Prerequisites

You'll need a C compiler to build and run this program. The code is written in C, so you can use compilers like GCC.

To use this Markov chain tweet generator, follow these steps:

1. Compile the program using a C compiler, e.g., `gcc`:
   ```bash
   gcc -o tweet_generator main.c markov_chain.c linked_list.c
   ```

2. Run the program with the following command:
   ```bash
   ./tweet_generator <seed> <num_tweets> <text_corpus_file> [num_words_to_read]
   ```

   - `<seed>`: An unsigned integer value to seed the random number generator.
   - `<num_tweets>`: The number of tweets to generate.
   - `<text_corpus_file>`: The path to the text corpus file containing the source text.
   - `[num_words_to_read]` (optional): The number of words to read from the text corpus (default is to read all words).

3. The program will generate and print random tweets to the standard output.

## Algorithm Overview

The Generic Markov Chain Text Generator uses a statistical approach to generate text based on the input data. Here's an overview of how the algorithm works:

1. Read Input Text: The program reads the input text data from a file specified by the user. It processes the text one word at a time, building a Markov chain of word transitions.

2. Build Markov Chain: The Markov chain is represented as a linked list of nodes. Each node represents a word, and it stores a list of words that can follow it in the input text. The program counts how often each word follows another word and stores this information in the chain.

3. Generate Random Sentences: To generate random sentences, the program starts with a random word from the input text and follows the chain to select the next word based on the transition probabilities. It continues selecting words until it reaches a predefined sentence length or encounters a word that typically ends a sentence.

4. Print Generated Sentences: The program prints the generated sentences to the console.

## Code Structure

The code is organized into multiple files:

- `main.c`: The main program file that handles command-line arguments, file I/O, and the overall program flow.
- `linked_list.c`: A library for managing linked lists, used to implement the Markov chain.
- `markov_chain.c`: Contains the implementation of the Markov chain and associated functions.

## Generic Programming

This program uses generic programming concepts to make the Markov chain adaptable for different data types. Specifically, it allows you to define custom input and output functions for different data types. Here's how you can use generic programming in this program:

- `markov_chain.h` includes function pointers for input and output functions that can be customized for various data types. For example:
  - `typedef void (*MC_InputFunction)(void*, FILE*);`: This defines an input function that reads data into a custom data structure (specified by `void*`) from a file.
  - `typedef void (*MC_OutputFunction)(const void*, FILE*);`: This defines an output function that writes data from a custom data structure (specified by `const void*`) to a file.

- You can create custom input and output functions for different data types by implementing functions with the same signature and passing them to the Markov chain functions when initializing or using the chain.

- The program demonstrates generic programming by providing sample input and output functions for text data (`MC_TextInput` and `MC_TextOutput`) in `markov_chain.c`. You can create similar functions for other data types, such as integers, if needed.

By customizing the input and output functions, you can use this program for various data types and adapt it to different text analysis tasks.
