"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def dest(mnem: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        # Your code goes here!
        if mnem == "":
            return "000"
        if mnem == "M":
            return "001"
        if mnem == "D":
            return "010"
        if mnem == "DM" or mnem == "MD":
            return "011"
        if mnem == "A":
            return "100"
        if mnem == "AM" or mnem == "MA":
            return "101"
        if mnem == "AD" or mnem == "DA":
            return "110"
        if mnem == "ADM":
            return "111"
        return ""

    @staticmethod
    def comp(mnem: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        # Your code goes here!
        if mnem == "0":
            return "0101010"
        if mnem == "1":
            return "0111111"
        if mnem == "-1":
            return "0111010"
        if mnem == "D":
            return "0001100"
        if mnem == "A":
            return "0110000"
        if mnem == "!D":
            return "0001101"
        if mnem == "!A":
            return "0110001"
        if mnem == "-D":
            return "0001111"
        if mnem == "-A":
            return "0110011"
        if mnem == "D+1":
            return "0011111"
        if mnem == "A+1":
            return "0110111"
        if mnem == "D-1":
            return "0001110"
        if mnem == "A-1":
            return "0110010"
        if mnem == "D+A":
            return "0000010"
        if mnem == "D-A":
            return "0010011"
        if mnem == "A-D":
            return "0000111"
        if mnem == "D&A":
            return "0000000"
        if mnem == "D|A":
            return "0010101"
        if mnem == "M":
            return "1110000"
        if mnem == "!M":
            return "1110001"
        if mnem == "-M":
            return "1110011"
        if mnem == "M+1":
            return "1110111"
        if mnem == "M-1":
            return "1110010"
        if mnem == "D+M":
            return "1000010"
        if mnem == "D-M":
            return "1010011"
        if mnem == "M-D":
            return "1000111"
        if mnem == "D&M":
            return "1000000"
        if mnem == "D|M":
            return "1010101"
        if mnem == "A<<":
            return "0100000"
        if mnem == "D<<":
            return "0110000"
        if mnem == "M<<":
            return "1100000"
        if mnem == "A>>":
            return "0000000"
        if mnem == "D>>":
            return "0010000"
        if mnem == "M>>":
            return "1000000"
        return ""

    @staticmethod
    def jump(mnem: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        # Your code goes here!
        if mnem == "":
            return "000"
        if mnem == "JGT":
            return "001"
        if mnem == "JEQ":
            return "010"
        if mnem == "JGE":
            return "011"
        if mnem == "JLT":
            return "100"
        if mnem == "JNE":
            return "101"
        if mnem == "JLE":
            return "110"
        if mnem == "JMP":
            return "111"
        return ""
