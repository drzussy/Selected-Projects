# From Nand to Tetris: Code Repository Overview

## Introduction

This repository presents an overview of my work in hardware description language (HDL) and low-level programming. It represents a comprehensive understanding of computer systems, from the fundamental hardware building blocks to low-level software development.

## Course Outline (Weeks 1-5)

Below is a concise summary of what is covered in this repository, by subdirectory:

### 1: Boolean Logic
- Implementation of basic logic gates (AND, OR, NOT etc.).
- Introduction to Boolean algebra.
- Building blocks of digital circuits.

### 2: Boolean Arithmetic
- Implementation of arithmetic operations using Boolean logic.
- Binary representation of numbers.
- Addition, subtraction, and multiplication at the binary level.

### 3: Sequential Logic
- Flip-flops and memory units.
- Design and construction of sequential circuits.
- Building registers, counters, and basic memory units.

### 4: The Von Neumann Architecture
- Overview of the Von Neumann architecture.
- Development of a simplified computer system.
- Components include an Arithmetic Logic Unit (ALU), a Central Processing Unit (CPU), and a basic memory system.

### 5: Machine Language
- Introduction to machine language programming.
- Representation of low-level assembly instructions.
- Writing programs in a custom assembly language tailored to the provided computer architecture.

### 6: Assembler Implementation With Python
- 3 modules; Parser, SymbolTable and Code that together are a program designed to translate code written in a symbolic machine language into code written in binary machine language.
- Use Main to run said code.
- To Run input: 

``` bash
Assembler <path>/file.asm
# or for all files in a directory
Assembler ~/nand/dir/
```
- output files will be <"filename">.hack
- test and compare files are in the test sub-directory
