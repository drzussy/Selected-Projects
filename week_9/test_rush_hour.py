from car import *
from board import *
from game import *


def test_board_init():
    board1 = Board()
    assert str(board1) == "[['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]"

    assert board1.cell_list() == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1), (
        3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)]


def test_board_unique():
    board1 = Board()
    board1.board = [['Y', 'Y', 'Y', 'E', 'E', 'E', 'E'], ['R', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'E', 'E', 'E', 'E', 'E', 'E'], [
        'R', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'O', 'O', 'O', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]
    assert board1._unique('R') == False
    assert board1._unique('G') == True


def test_board_in_board():
    board1 = Board()
    assert board1._in_board((0, 0)) == True
    assert board1._in_board((10, 0)) == False
    assert board1._in_board((7, 7)) == False
    assert board1._in_board((0, 6)) == True


def test_board_possible_moves():
    board1 = Board()


def test_board_add_car():
    board1 = Board()
    car1 = Car("R", 3, (0, 0), 0)
    car2 = Car("B", 2, (1, 1), 0)
    car3 = Car("O", 4, (2, 3), 1)
    car4 = Car("R", 2, (3, 0), 1)
    car5 = Car("G", 3, (1, 0), 0)

    assert board1.add_car(car1) == True
    assert board1.cars_on_board == {car1.get_name(): car1}
    assert board1.board == [['R', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'E', 'E', 'E', 'E', 'E', 'E'], [
        'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]

    assert board1.add_car(car2) == True
    assert board1.cars_on_board == {
        car1.get_name(): car1, car2.get_name(): car2}
    assert board1.board == [['R', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'E', 'E', 'E', 'E'], [
        'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]

    assert board1.add_car(car3) == True
    assert board1.cars_on_board == {
        car1.get_name(): car1, car2.get_name(): car2, car3.get_name(): car3}
    assert board1.board == [['R', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'O', 'O', 'O', 'O'], [
        'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]
    assert board1.add_car(car4) == False
    assert board1.cars_on_board == {
        car1.get_name(): car1, car2.get_name(): car2, car3.get_name(): car3}
    assert board1.add_car(car5) == False
    assert board1.cars_on_board == {
        car1.get_name(): car1, car2.get_name(): car2, car3.get_name(): car3}
    assert board1.move_car('R', "d")


def check_possible_moves():
    car1 = Car("R", 3, (0, 0), 0)
    car2 = Car("B", 2, (1, 1), 0)
    car3 = Car("O", 4, (2, 3), 1)
    car4 = Car("R", 2, (3, 0), 1)
    car5 = Car("G", 3, (1, 0), 0)
    board1 = Board()

    assert board1.possible_moves() == []
    board1.add_car(car1)
    assert board1.possible_moves() == [("R", "d", "can move to (3, 0)")]
    board1.add_car(car2)
    assert board1.possible_moves() == [("R", "d", "can move to (3, 0)"), (
        "B", 'u', "can move to (0, 1)"), ("B", "d", "can move to (3, 1)")]
    board1.add_car(car3)
    assert board1.possible_moves() == [("R", "d", "can move to (3, 0)"), (
        "B", 'u', "can move to (0, 1)"), ("B", "d", "can move to (3, 1)"), ("O", "l", "can move to (2, 2)")]


cars = [Car("R", 3, (0, 0), 0),
        Car("B", 2, (1, 1), 0),
        Car("O", 4, (2, 3), 1),
        Car("R", 2, (3, 0), 1),
        Car("G", 3, (1, 0), 0)]


def test_board_move_car():
    board1 = Board()
    for car in cars:
        board1.add_car(car)
    assert board1.move_car("R", "u") == False
    assert board1.move_car("R", "d")
    assert board1.board == [['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'O', 'O', 'O', 'O'], [
        'R', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]
    assert board1.move_car("o", 'r') == False
    assert board1.move_car('O', 'l')
    assert board1.board == [['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'E', 'E', 'E', 'E', 'E'], ['R', 'B', 'O', 'O', 'O', 'O', 'E'], [
        'R', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E']]
    assert board1.move_car('O', 'l') == False


car1 = Car("R", 3, (0, 0), 0)
car2 = Car("B", 2, (1, 1), 0)
car3 = Car("O", 4, (2, 3), 1)


def test_car(car1, car2):
    # get_name
    assert car1.get_name() == "R"
    # get_coordinates
    assert car1.car_coordinates() == [(0, 0), (1, 0), (2, 0)], print(
        car1.car_coordinates())
    assert car2.possible_moves() == {"u": "move up to (0, 1)", "d": "move down to (3, 1)"}, print(
        "should have got" + str(car2.possible_moves()))

    # movement requirments

    assert car1.possible_moves() == {'u': "move up to (-1, 0)", 'd': "move down to (3, 0)"}, print(
        "should have got" + str(car1.possible_moves()))


def test_movement_requirements(*args):

    assert car2.movement_requirements("u") == [(0, 1)]


def test_car_move(*args):
    assert car1.move('u') == True
    assert car1.location == (-1, 0)
    car1.location = (0, 0)
    assert car1.move('d') == True
    assert car1.location == (1, 0)
    car1.location = (0, 0)
    assert car1.move('r') == False
    assert car1.move("") == False
    assert car3.move("u") == False
    assert car3.move("r") == True
    assert car3.location == (2, 4)
    assert car3.move("l") == True
    assert car3.location == (2, 3)
    assert car3.move('r') == True
    assert car3.location == (2, 4), print(car3.location)
    car3.location == (2, 3)


test_board_init()
test_board_in_board()
test_board_unique()
test_car(car1, car2)
test_movement_requirements(car1, car2)
test_car_move(car1, car2, car3)
test_board_add_car()
test_board_possible_moves()
test_board_move_car()
