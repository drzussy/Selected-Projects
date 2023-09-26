"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing

# from nand2tetris.06.Parser import L_COMMAND
from SymbolTable import *
from Parser import *
from Code import *


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # initialize parser
    parser = Parser(input_file)
    # all white spaces and comments are deleted

    # initialize symbol_table
    symbol_table = SymbolTable()

    # first iteration of code - find all L_COMMANDS and add to symbol_table
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == L_COMMAND:
            symbol_table.add_entry(parser.symbol(), parser.cur_line+1)

    # second iteration of code - translating @variable symbols
    while parser.has_more_commands():
        parser.advance()

        # find all A_COMMANDS
        if parser.command_type() == A_COMMAND:
            cur_symbol = parser.symbol()

            # if variable_symbol is already seen, replace with its value
            if symbol_table.contains(cur_symbol):
                parser.text[parser.cursor] = "@" + \
                    str(symbol_table.get_address(cur_symbol))

            # if not already seen, make sure its not a direct address
            elif not cur_symbol.isdigit():
                # if new variable, add to symbol table by current empty spot (after 15)
                symbol_table.add_entry(cur_symbol, symbol_table.cur_empty)
                # increment cur_empty
                symbol_table.cur_empty += 1

    # symbol table is complete.
    # all variables are swapped

    while parser.has_more_commands():
        parser.advance()
        cur_bin = ""
        command = parser.command_type()

        if command == A_COMMAND:
            desired_length = 15
            cur_bin += "0"
            # in symbol_table
            if symbol_table.contains(parser.current_command[1:]):
                num_in_binary = bin(symbol_table.get_address(
                    parser.current_command[1:]))[2:]
            # not in symbol_table
            else:
                cur_address = int(parser.current_command[1:])
                num_in_binary = bin(cur_address)[2:]
            # pad binary number with zeros
            if len(num_in_binary) < desired_length:
                zero_dif = desired_length-len(num_in_binary)
                cur_bin += "0"*zero_dif

            cur_bin += num_in_binary

        elif command == C_COMMAND:
            # check for shift command
            if "<<" in parser.current_command or ">>" in parser.current_command:
                cur_bin += "101"
            # not shift
            else:
                cur_bin += "111"
            # for either shift or regular command
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            # instance of Code()
            codify = Code()
            # assemble full command
            cur_bin += codify.comp(comp) + codify.dest(dest) \
                + codify.jump(jump)
        # for L_COMMAND skip so as not to add empty line
        if command != L_COMMAND:
            output_file.write(cur_bin + "\n")


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
