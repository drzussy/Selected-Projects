#############################################################
# FILE : ex7.py
# WRITER : noam susman , noam.susman , 318528304
# EXERCISE : intro2cs1 ex7 2023
# DESCRIPTION: 9 recursive functions
# STUDENTS I DISCUSSED THE EXERCISE WITH: dovi teitler
# WEB PAGES I USED: geeksforgeeks
# NOTES: yikes
#############################################################

from operator import truediv
import string
import typing
from typing import Any, List
from ex7_helper import *

# N = typing.TypeVar('N', int, float)


# 1
def mult(x: N, y: int) -> N:
    # base case
    if y == 0:
        return 0
    # move towards base case
    result: N = add(x, mult(x, subtract_1(y)))

    return result


def _is_even_helper(n: int) -> int:
    '''subtracts 2'''
    n = subtract_1(subtract_1(n))
    return n


# 2
def is_even(n: int) -> bool:
    '''Check if a positive integer is even or not using a recursive method'''
    # base case
    if n == 0:
        return True
    if n == 1:
        return False
    if is_even(_is_even_helper(n)):
        return True
    else:
        return False


# 3
def log_mult(x: N, y: int) -> N:
    '''Multiply two numbers with a logarithmic runtime'''

    if y == 0 or x == 0:
        return 0
    # base case
    if y == 1:
        return x
    # progress through recursion
    if is_odd(y):
        sum = log_mult(x, divide_by_2(y))
        # add also x since divide_by_2 will erase it
        return add(add(sum, sum), x)
    else:
        sum = log_mult(x, divide_by_2(y))
        return add(sum, sum)


# 4
def is_power(b: int, x: int) -> bool:
    '''Checks if exists a non negative number 'n' so that b by the power of n equals to x
    and if so return True'''
    return _is_power_helper(b, x, b)


def _is_power_helper(b: int, x: int, power: int) -> bool:
    # base case
    if power != 0 and x == 1:
        return True
    if power == x or power == 0 and x == 0 or power == 0 and x == 1:
        return True
    if power > x or power == 0 or power == 1 and x != 1:
        return False

    # check is power on b**2 and check again
    if _is_power_helper(b, x, log_mult(power, b)):
        return True
    return False


# 5
def reverse(s: str) -> str:
    t: str = ""
    return _reverse_helper(s, t)


def _reverse_helper(s: str, rev_string: str) -> str:
    if len(rev_string) == len(s):
        return rev_string
    rev_string = append_to_end(
        rev_string, s[len(s) - len(rev_string) - 1])
    return _reverse_helper(s, rev_string)


# 6
def play_hanoi(hanoi: Any, n: int, src: Any, dest: Any, temp: Any) -> None:
    '''algorithm for hanoi_game.py'''

    # base case
    if n > 0:
        # hanoi.move(src, dest)
        # easier problem
        play_hanoi(hanoi, n-1, src, temp, dest)
        # move bottom to empty rod
        hanoi.move(src, dest)
        # move others back to now original and now empty rod
        play_hanoi(hanoi, n-1, temp, dest, src)
    ...


# 7
def number_of_ones(n: int) -> int:
    '''count number of ones in all numbers from 0 to n'''
    counter: int = 0
    if n == 0:
        return 0
    return _helper_number_of_ones(n, counter)


def _helper_number_of_ones(n: int, counter: int) -> int:
    '''iterate over all numbers from 0 to n'''
    # base
    if n <= 1:
        return counter + 1
    counter += _helper_number_of_ones(n-1, counter)
    # for each number check how many ones are in it
    counter = _count_ones_in_number(n, counter)

    return counter


def _count_ones_in_number(n: int, counter: int) -> int:
    '''check how many 1's are in a given number'''
    # base
    if n == 0:
        return counter
    # recurse until n<=0 and then for each whole division of ten check if last number is a 1
    counter = _count_ones_in_number(n // 10, counter)
    if n % 10 == 1:
        return counter + 1
    return counter


# 8

def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    # base cases
    if l1 == [] and l2 == []:
        return True
    if l1 == [] or l2 == []:
        return False
    if len(l1) != len(l2):
        return False
    j = 0
    return _compare_2d_lists_helper(l1, l2, j)


def _compare_2d_lists_helper(l1: List[List[int]], l2: List[List[int]], j: int) -> bool:
    # base case
    if j == len(l1):
        return True
    i: int = 0
    if not _compare_1d_list(l1[j], l2[j], i):
        return False
    return _compare_2d_lists_helper(l1, l2, j+1)


def _compare_1d_list(inner_l1: List[int], inner_l2: List[int], i: int) -> bool:
    if len(inner_l1) != len(inner_l2):
        return False
    if i == len(inner_l1):
        return True
    if inner_l1[i] != inner_l2[i]:
        return False
    return _compare_1d_list(inner_l1, inner_l2, i + 1)


def magic_list(n: int) -> list[Any]:
    # base case
    i: int = 0
    top_list: list[None] = []
    top_list = _helper_magic_list(n, top_list)
    return top_list


def _helper_magic_list(n: int, top_list: Any) -> Any:
    if n == 0:
        return top_list
    # top_list = top_list + [magic_list(n - 1)]
    return _helper_magic_list(n-1, [magic_list(n - 1)] + top_list)
