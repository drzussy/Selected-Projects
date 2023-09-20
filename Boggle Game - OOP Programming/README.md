# Boggle Game

This repository contains a Python implementation of the classic word game, Boggle. Boggle is a word search game where players search for words on a grid of letters.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Game Logic](#game-logic)
  - [Boggle Class](#boggle-class)
  - [Board Class](#board-class)
  - [Game Class](#game-class)
- [Usage](#usage)
- [Requirements](#requirements)
- [Installation](#installation)
- [License](#license)

## Introduction

Boggle is a popular word game that challenges players to find as many words as possible by connecting adjacent letters on a grid. This implementation of Boggle includes a graphical user interface (GUI) and various features to enhance the gaming experience.

## Features

- **Interactive GUI**: The game features a user-friendly graphical interface that allows players to click on letters to form words.

- **Word Validation**: The game validates player-entered words against a dictionary of valid words.

- **Timer**: A timer keeps track of the remaining time for each game session.

- **Score Tracking**: The game tracks the player's score based on the length of words found.

- **Word List**: Found words are displayed on the GUI, helping players keep track of their progress.

- **Randomized Boards**: Boggle boards are randomly generated for each game, providing a unique gameplay experience.

## Game Logic

### Boggle Class

- **Initialization**: The `Boggle` class initializes the game. It creates instances of the `Game` and `GUI` classes, sets up the GUI, and assigns actions to buttons and squares on the board.

- **create_square_functionality()**: This method creates functionality for each square on the Boggle board. When a player clicks on a square, this function determines what action to take based on the game's logic.

- **start_boggle()**: This method is triggered when the "Start Game" button is clicked. It activates the game board and starts the timer.

- **reset_boggle()**: This method is triggered when the "New Game" button is clicked. It resets the game to its initial state.

- **run()**: This method starts the GUI's main event loop, allowing the player to interact with the game.

### Board Class

- **Initialization**: The `Board` class initializes the Boggle board. It randomly generates a 4x4 grid of letters.

- **check_in_board()**: Checks if a given tuple of coordinates is within the boundaries of the game board.

- **cell_content()**: Returns the letter at a specific board coordinate.

- **check_adj()**: Checks if two coordinates are adjacent to each other on the board.

- **update_path()**: Updates the current word path on the board with a new coordinate. Returns `True` if the path was updated.

- **get_current_path()**: Returns the current word path as a list of coordinates.

- **get_board()**: Returns the game board.

- **reset_path()**: Resets the current word path.

- **reset_board()**: Generates a new random Boggle board.

### Game Class

- **Initialization**: The `Game` class initializes the game's logic. It creates a dictionary of valid words from a text file, initializes the game board, and sets up other game variables.

- **create_words_dict()**: Reads a list of valid words from the `boggle_dict.txt` file and creates a dictionary of words with initial state as `False`.

- **words_on_board()**: Finds all valid words present on the current game board using a recursive helper function from `ex11_utils.py`.

- **update_current_word()**: Updates the current word being formed by the player based on the path on the board.

- **reset_current_word()**: Resets the current word being formed.

- **submit_word()**: Submits the current word and checks if it's valid. If valid, updates the score and word lists.

- **update_game()**: Updates the game state based on player actions. Returns different codes indicating the result of the action (e.g., word found, not a word).

- **reset_game()**: Resets the game to its initial state, including the board and game variables.

## Usage

To play the game, follow these steps:

1. Run the `boggle.py` script.
2. Click on adjacent letters to form words.
3. Submit words by clicking the "Submit" button.
4. The game will validate your word and update your score.
5. Try to find as many words as possible before the timer runs out.

## Requirements

- Python 3.x
- tkinter (for the GUI)

## Installation

1. Clone this repository to your local machine using `git clone`.
2. Install the required dependencies by running:

   ```bash
   pip install -r
