#############################################################
# FILE : puzzle_solver.py
# WRITER : noam susman , noam.susman , 318528304
# EXERCISE : intro2cs1 ex8 2023
# DESCRIPTION: reucrsive functions to solve shachor uftor
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: fun fun fun
#############################################################

from typing import List, Tuple, Set, Optional


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_first_seen(picture: Picture, row: int, col: int) -> int:
    '''find first cell in row (from left) and col (from top) that isnt black. undecided (-1) is considered white (1)'''
    for i in range(col, -1, -1):
        if picture[row][i] == 0:
            first_in_row: int = i + 1
            break
        if i == 0:
            first_in_row = 0
    for i in range(row, -1, -1):
        if picture[i][col] == 0:
            first_in_col: int = i + 1
            break
        if i == 0:
            first_in_col = 0
    return first_in_col, first_in_row


def max_seen_counter(picture: Picture, row: int, col: int, first_in_row: int, first_in_col: int) -> int:
    '''counts max seen cells in row and column. undecided (-1) are considered white (1)'''
    # firsts = first_col, first_row
    # parameters = width, height
    pic_width: int = len(picture[0])
    pic_height: int = len(picture)
    counter: int = 0
    # count seen in column by strating at cell and working back
    for i in range(first_in_col, pic_height):
        if picture[i][col] == 0:
            break
        counter += 1
    # count seen in row
    for i in range(first_in_row, pic_width):
        if picture[row][i] == 0:
            break
        counter += 1
    return counter

# 1


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    '''Find number of seen cells from current cell. Any unkown cell will be considered as a white cell.
    Parameters are a Picture: Picture, Row number: int, Column number:int '''
    # if black_cell(picture, row, col):
    if picture[row][col] == 0:
        return 0
    # find first seen square in row from left and col from bottom:
    first_in_col, first_in_row = max_first_seen(picture, row, col)
    # count from first until first black
    seen = max_seen_counter(picture, row, col, first_in_row, first_in_col)
    # if counter is 1 then cell sees only itself otherwise it counted itself so take off 1
    if seen == 1:
        return 1
    return seen - 1
    ...


def min_first_seen(picture: Picture, row: int, col: int) -> tuple[int, int]:
    '''find first cell in row (from left) and col (from top) that isnt black. undecided (-1) is considered black (0)'''
    for i in range(col, -1, -1):
        if picture[row][i] != 1:
            first_in_row: int = i + 1
            break
        if i == 0:
            first_in_row = 0
    for i in range(row, -1, -1):
        if picture[i][col] != 1:
            first_in_col: int = i + 1
            break
        if i == 0:
            first_in_col = 0
    return first_in_col, first_in_row


def min_seen_counter(picture: Picture, row: int, col: int, first_in_row: int, first_in_col: int) -> int:
    '''counts max seen cells in row and column. undecided (-1) are considered black (0)'''
    # firsts = first_col, first_row
    # parameters = width, height
    pic_width = len(picture[0])
    pic_height = len(picture)
    counter: int = 0
    # count seen in column by strating at cell and working back
    for i in range(first_in_col, pic_height):
        if picture[i][col] != 1:
            break
        counter += 1
    # count seen in row
    for i in range(first_in_row, pic_width):
        if picture[row][i] != 1:
            break
        counter += 1
    return counter


# 2
def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    '''Find number of seen cells from current cell. Any unkown cell will be considered as a black cell.
    Parameters are a Picture: Picture, Row number: int, Column number:int '''
    if picture[row][col] != 1:
        return 0
    # find first in column and row
    first_in_col, first_in_row = min_first_seen(picture, row, col)
    counter: int = 0
    seen: int = min_seen_counter(picture, row, col, first_in_row, first_in_col)
    if seen == 1:
        return seen
    return seen - 1
    ...


def _check_restraints_helper(picture, constraint, result) -> int:
    '''recieves a specific constraint and checks if its cells keep to its constraints or not'''
    if result == 0:
        return 0
    min_seen: int = min_seen_cells(picture, constraint[0], constraint[1])
    max_seen: int = max_seen_cells(picture, constraint[0], constraint[1])
    # min == max
    if min_seen == constraint[2] and max_seen == constraint[2]:
        return 1
    # between min and max
    if min_seen <= constraint[2] and constraint[2] <= max_seen:
        return 2
    # beyond constraints
    if constraint[2] < min_seen or max_seen < constraint[2]:
        return 0

# 3


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    '''Iterate over all constraints in a constraints set and check that each one is kept.
    returns 0 if not kept, returns 1 all constraints are exactly kept, returns 2 if restraints are kept but not exactly'''
    result: int = 1
    for constraint in constraints_set:
        temp: int = _check_restraints_helper(picture, constraint, result)
        if type(temp) == int:
            if temp == 0:
                return temp
            if temp > result:
                result = temp
    return result
    ...


def make_board(rows: int, cols: int) -> Picture:
    '''initilize a starter board of undetermined squares of (-1)'''
    return [[-1 for col in range(cols)] for row in range(rows)]


def move_to_next(n: int, m: int, row: int, col: int) -> tuple:
    if col < m - 1:
        col += 1
    else:
        row += 1
        col: int = 0
    return row, col


def _solve_puzzle_helper(row, col, n: int, m: int, picture: Picture, constraints_set: Set[Constraint]) -> Picture:
    '''helper function to recursively find a solution to a puzzle.'''

    # base case
    if row == n - 1 and col == m or row == n:
        return True
    # if finished trying go back
    if picture[row][col] == 1:
        picture[row][col] = -1
        return False

    # mark square next option
    picture[row][col] += 1
    # check
    check: int = check_constraints(picture, constraints_set)
    if check == 1:
        return True
    if check == 0:
        return False
    if check == 2:
        # move to next
        # check if next square is in the same row or the next
        row, col = move_to_next(n, m, row, col)
        # try for each option
        for i in range(2):
            if _solve_puzzle_helper(row, col, n, m, picture, constraints_set):
                return True
        # if not white or black reset square to undetermined and bactrack up to previous squares
        else:
            picture[row][col] = -1
            return False


def finish_board(picture) -> None:
    '''If all constraints are perfectly kept, turn all other squares to black'''
    for i in range(len(picture)):
        for j in range(len(picture[0])):
            if picture[i][j] == -1:
                picture[i][j] = 0


# 4
def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    '''Find a solution to the puzzle using backtracking. Enter constraint set and  '''
    if len(constraints_set) > n*m:
        return
    row: int = 0
    col: int = 0
    picture: List[List[int]] = make_board(n, m)
    if _solve_puzzle_helper(row, col, n, m, picture, constraints_set) or _solve_puzzle_helper(row, col, n, m, picture, constraints_set):
        finish_board(picture)
        return picture
    else:
        return None


def _how_many_helper(row, col, n, m, picture: Picture, constraints_set: Constraint, counter: List) -> bool or None:
    '''finish whole puzzle, check that its a valid solution and update counter list'''
    if row == n - 1 and col == m or row == n:
        return False
    # if finished trying go back
    if picture[row][col] == 1:
        picture[row][col] = -1
        return False

    # mark square next option
    picture[row][col] += 1
    check = check_constraints(picture, constraints_set)
    # check
    if check == 0:
        return False
    if check == 2 or check == 1:
        # check if at end of puzzle
        if check == 1 and (n - 1 == row and m - 1 == col):
            counter[0] += 1
        # move to next
        # check if next square is in the same row or the next
        row, col = move_to_next(n, m, row, col)
        # try for each option
        for i in range(2):
            if _how_many_helper(row, col, n, m, picture, constraints_set, counter):
                return True
        # if not white or black reset square to undetermined and bactrack up to previous squares
        if row < n and col < m:
            picture[row][col] = -1
        return False


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    '''receive a set of constraints and a board size (rows, cols) and return number of valid solutions to board. Uses a recursive helper function _how_many_solutions_helper.'''
    # if too many constraint return None
    if len(constraints_set) > n*m:
        return
    # initialize variables
    row = 0
    col = 0
    # initialize a board of undetermined (-1)
    picture: List[List[int]] = make_board(n, m)
    counter = [0]
    # check for first square 0 and 1
    for i in range(2):
        _how_many_helper(
            row, col, n, m, picture, constraints_set, counter)
    # after goimg through all solutions return counter
    return counter[0]


def minimize_constraint_set(constraints: Set[Constraint], rows, cols) -> Set[Constraint]:
    temp: Set[Constraint] = constraints.copy()
    for constraint in constraints:
        temp.remove(constraint)
        if how_many_solutions(temp, rows, cols) == 1:
            continue
        temp.add(constraint)
    return temp


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    '''This function receives a picture of a solved board and returns a set of constraints that matches the board'''
    constraints = set()
    # for each square generate a constraint until number of solutions is equal to one
    rows: int = len(picture)
    cols: int = len(picture[0])
    solutions: int = 0
    # get a set of constraints
    for row in range(rows):
        for col in range(cols):
            constraints.add((row, col, max_seen_cells(picture, row, col)))
            solutions = how_many_solutions(constraints, rows, cols)
            if solutions == 1:
                break
        if solutions == 1:
            break
    # minimize set
    constraints: Set[Constraint] = minimize_constraint_set(
        constraints, rows, cols)
    # return final set of constraints
    return constraints
