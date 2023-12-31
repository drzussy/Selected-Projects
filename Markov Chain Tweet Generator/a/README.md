# Markov Chain Tweet Generator

This project is a Markov chain-based tweet generator written in C. It reads text data from a file, builds a Markov chain model, and generates random tweets based on the learned patterns.

## Table of Contents

- [Usage](#usage)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [How it Works](#how-it-works)
## Usage

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

## Project Structure

The project consists of several source code files:

- `main.c`: The main program that handles command-line arguments, file input/output, and tweet generation.
- `markov_chain.c` and `markov_chain.h`: Implement the Markov chain data structure and related functions.
- `linked_list.c` and `linked_list.h`: Implement a linked list data structure used for building the Markov chain.
- `Makefile`: A Makefile for compiling the project.

## Dependencies

This project has no external dependencies other than the standard C library.

## How it Works

1. The program reads text data from a specified text corpus file, tokenizes it into words, and builds a Markov chain data structure to model the relationships between words.

2. You can specify the seed value for the random number generator, the number of tweets to generate, and the path to the text corpus file as command-line arguments.

3. The program generates random tweets based on the learned Markov chain model. It starts with a random word and selects the next word based on the frequency of occurrence in the training data.

4. Tweets are generated until they reach a maximum length or end with a period (.), ensuring that each tweet is a coherent sentence.

