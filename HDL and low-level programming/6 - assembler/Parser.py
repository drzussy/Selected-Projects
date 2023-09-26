"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

A_COMMAND = "A"
C_COMMAND = "C"
L_COMMAND = "L"


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """
    # class variables
    text: list = []
    # cursor is used to parse through input text
    cursor = -1
    # current command is the line where cursor is pointing to
    current_command: str = ""
    # cur_line is the current line in code if we ignore l_commands
    cur_line = -1

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        input_lines: list[str] = input_file.read().splitlines()
        for line in input_lines:
            parts = line.split("//")
            if not self.comment_or_white(parts[0]):
                # add to dict
                self.text.append(parts[0].replace(" ", ""))

    def comment_or_white(self, line) -> bool:
        i = 0
        for char in line:
            if char != " ":
                return False
        return True

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if self.cursor < len(self.text) - 1:
            return True
        # moved the cursor reset to here from advance (the while logic in main dictated)
        self.cursor = -1
        self.current_command = ""
        self.cur_line = -1
        return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.cursor += 1
            self.current_command = self.text[self.cursor]

            if self.command_type() != L_COMMAND:
                self.cur_line += 1

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        for char in self.current_command:
            if char == "@":
                return A_COMMAND
            elif char == "(":
                return L_COMMAND
            # assume no errors in file so must be c_command
            else:
                return C_COMMAND
        return ""

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        # if a command
        if self.command_type() == A_COMMAND:
            return self.current_command[1:]
        # if L command
        elif self.command_type() == L_COMMAND:
            return self.current_command[1:-1]
        else:
            return ""

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == C_COMMAND:
            if "=" in self.current_command:
                parts = self.current_command.split("=")
                return parts[0]
            else:
                return ""
        return ""

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == C_COMMAND:
            if "=" in self.current_command:
                parts: list[str] = self.current_command.split("=")
                # split by ";" and return the string before
                return parts[1].split(";")[0]
                # else:
                #     return parts[1]
            elif ";" in self.current_command:
                parts: list[str] = self.current_command.split(";")
                return parts[0]
            else:
                return ""
        return ""

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if ";" in self.current_command:
            parts = self.current_command.split(";")
            return parts[1]
        else:
            return ""
