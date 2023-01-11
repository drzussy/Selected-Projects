from puzzle_solver import *

Picture = List[List[int]]
Constraint = Tuple[int, int, int]
picture: Picture = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]


def max_seen_cells_tests() -> None:
    assert max_seen_cells(picture, 0, 0) == 1
    assert max_seen_cells(picture, 1, 0) == 0
    assert max_seen_cells(picture, 1, 2) == 5
    assert max_seen_cells(picture, 1, 1) == 3


def min_seen_cells_tests() -> None:
    assert min_seen_cells(picture, 0, 0) == 0
    assert min_seen_cells(picture, 1, 0) == 0
    assert min_seen_cells(picture, 1, 2) == 0
    assert min_seen_cells(picture, 1, 1) == 1


def check_constraints_test() -> None:
    picture1: Picture = [[-1, 0, 1, -1], [0, 1, -1, 1], [1, 0, 1, 0]]
    picture2: Picture = [[0, 0, 1, 1], [0, 1, 1, 1], [1, 0, 1, 0]]
    assert check_constraints(picture1, {(0, 3, 5), (1, 2, 5), (2, 0, 1)}) == 0
    assert check_constraints(picture2, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 1
    assert check_constraints(picture1, {(0, 3, 3), (1, 2, 5), (2, 0, 1)}) == 2


if __name__ == "__main__":
    max_seen_cells_tests()
    min_seen_cells_tests()
    check_constraints_test()
