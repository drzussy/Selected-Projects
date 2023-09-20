# Project 6 - MLP Network Image Classification

Welcome to my custom Multi-Layer Perceptron (MLP) network image classification program. This project demonstrates my programming skills in C++ and showcases my ability to implement and utilize neural networks for image classification.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Network Architecture](#network-architecture)
- [Testing](#testing)

## Introduction

This program implements an MLP network for image classification. It loads pre-trained weights and biases for the network's layers and provides a command-line interface (CLI) for image classification. The code is organized and well-structured to ensure readability and maintainability.

## Prerequisites

To run this program, you'll need a C++ compiler. You can compile and execute the code on your local machine.

## Usage

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/mlp-network-image-classification.git
   ```

2. Navigate to the project directory:

   ```bash
   cd mlp-network-image-classification
   ```

3. Compile the program:

   ```bash
   g++ -o mlpnetwork main.cpp Matrix.cpp MlpNetwork.cpp Dense.cpp Activation.cpp -std=c++11
   ```

4. Run the program:

   ```bash
   ./mlpnetwork weights/w1 weights/w2 weights/w3 weights/w4 biases/b1 biases/b2 biases/b3 biases/b4
   ```

   Replace `weights/w1`, `weights/w2`, `weights/w3`, `weights/w4`, `biases/b1`, `biases/b2`, `biases/b3`, and `biases/b4` with the actual paths to the weight and bias files for your MLP network.

5. Follow the program's prompts to input an image path. The program will classify the image using the MLP network and display the results.

## Code Structure

The code is well-structured and organized into several files:

- `main.cpp`: This is the main program file that handles command-line arguments, user input, and the overall program flow.
- `Matrix.cpp`: Contains the implementation of the `Matrix` class, a fundamental component for matrix operations in the network.
- `MlpNetwork.cpp`: This file houses the implementation of the `MlpNetwork` class, where the MLP network architecture and classification logic are defined.
- `Dense.cpp`: The `Dense` class is implemented in this file, representing a dense layer in the MLP network.
- `Activation.cpp`: Contains various activation functions used throughout the network.

## Network Architecture

I have designed the MLP network architecture in the `MlpNetwork` class within the `MlpNetwork.cpp` file. The network comprises four dense layers:

- Layer 1: Input layer with 784 neurons (corresponding to a 28x28 image).
- Layer 2: Hidden layer with 128 neurons and ReLU activation.
- Layer 3: Hidden layer with 64 neurons and ReLU activation.
- Layer 4: Output layer with 10 neurons and softmax activation (for digit classification).

The program loads pre-trained weights and biases for each layer from binary files provided as command-line arguments. It's important to ensure that the weights and biases files match the expected dimensions based on the network architecture.

## Testing

In addition to the main program, I have also included a test file, `test.cpp`, which tests various aspects of the code, including the `Matrix` class and other functionalities. This test file demonstrates my commitment to code quality and reliability.
