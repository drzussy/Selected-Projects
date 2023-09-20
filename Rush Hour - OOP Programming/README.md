
#Rush Hour Game

## Overview

This project implements a simplified version of the classic puzzle game "Rush Hour" using Python and object-oriented programming principles. In the Rush Hour game, players are presented with a grid-based board containing vehicles of different sizes. The goal is to maneuver a specific vehicle (usually a red car) to the exit by sliding other vehicles out of the way.

![Rush Hour Game](rushhour_game.png)

## Files

The project consists of the following Python files:

- **board.py**: This file defines the `Board` class, which represents the game board. The board contains information about the positions of all vehicles and provides methods for making moves and checking for victory conditions.

- **car.py**: The `Car` class is defined in this file. Each car on the board is represented as an instance of this class. It includes properties such as color, length, and position, as well as methods for calculating possible moves and updating the car's position.

- **game.py**: The `Game` class, defined in this file, is responsible for managing the game itself. It handles user input, controls the flow of the game, and checks for victory conditions.

- **helper.py**: This utility file contains a function named `load_json`, which reads a JSON file and returns its contents as a dictionary. This is used for loading initial car configurations.

## How to Play

Follow these steps to play the Rush Hour game:

1. Make sure you have Python installed on your computer.

2. Navigate to the directory containing the game files.

3. Run the game by executing the following command in your terminal or command prompt:

   ```bash
   python game.py
   ```

4. The game will start, and you will see the initial game board displayed in the terminal.

5. You can make moves by entering commands in the format `[Color][Direction]`, where `[Color]` is the color of the car you want to move, and `[Direction]` is the direction in which you want to move it (e.g., "BRU" to move the blue car up).

6. Continue making moves until you successfully clear a path for the target car (usually the red car) to reach the exit.

## Victory Condition

The game is won when you successfully maneuver the target car to the exit. At this point, the game will display a victory message, and you will have solved the puzzle.

## Custom Car Configurations

You can create custom car configurations by modifying the `car_config.json` file. This JSON file contains information about the initial placement of cars on the game board. Each car is represented as an object with properties like "color," "length," "position," and "orientation."

## Acknowledgments

This Rush Hour game project is inspired by the classic puzzle game of the same name. It serves as a fun exercise in object-oriented programming and logic puzzle-solving.