from car import *
from game import *
from typing import *


class Board:
    """
    class of type board. 
    attributes:
    board = list of lists of chars that indicate presence of a car
    cars_on_board = dict of all cars on the board (name_of_car: car_object)
    to be used by game object to play Rush Hour game.
    methods:
    __init__ - intializes a board object
    __str__ - converts presentation of object in a string
    cell_list - returns a list of all coordinates on the board
    _in_board - hidden method. checks if a coordinate is in board
    _unique - checks if theres a another car with same color
    possible_moves - returns all legal moves of cars in board

    """
    SIZE: int = 7

    def __init__(self):
        self.board: List[List[str]] = Board._generate_board()
        self.cars_on_board = {}

    def _generate_board():
        '''its in the name'''
        board: List[List[str]] = [['E' for i in range(Board.SIZE)]
                                  for j in range(Board.SIZE)]
        board[3] += ["E"]
        return board

    def __str__(self) -> str:
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        final_string = "["
        for row in self.board:
            final_string += str(row)
            final_string += ",\n"
        final_string = final_string[:-1]
        final_string += "]"
        return final_string

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # from (0,0) to (6,6) and the target cell (3,7)
        coordinates = []
        target_row, target_col = self.target_location()
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                coordinates.append((i, j))
                # add target cell
                if i == target_row and j == target_col - 1:
                    coordinates.append((target_row, target_col))
        return coordinates

    def _in_board(self, coor) -> bool:
        '''check that coor is within board edges'''
        if coor[0] == 3 and coor[1] == 7:
            return True
        if 0 <= coor[0] <= Board.SIZE - 1 and 0 <= coor[1] <= Board.SIZE - 1:
            return True
        return False

    def _unique(self, color) -> bool:
        '''checks if a car with color 'color' is already on the board'''
        board: List[List[str]] = self.board
        for row in board:
            for col in row:
                if col == color:
                    return False
        return True

    def possible_moves(self) -> List:
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]

        # board has a dict of cars on the board
        # for each car in dict get the possible moves, validate them and add to list
        legal_moves: List = []
        # access cars from dict{name:car_object}
        for name in self.cars_on_board:
            car: Car = self.cars_on_board[name]
            # dict of possible moves for this car
            all_moves: Dict = car.possible_moves()
            # iterate for each direction
            for move_key in all_moves:
                # get the cell the car will be moved to in this direction
                for cell in car.movement_requirements(move_key):
                    if self._in_board(cell):
                        legal_moves.append(
                            (name, move_key, f"can move to {cell}"))
        return legal_moves

    def target_location(self) -> tuple:
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return (3, 7)

    def cell_content(self, coordinate: tuple):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if len(self.board) != 0:
            row: int = coordinate[0]
            col: int = coordinate[1]
            if self.board[row][col] == 'E':
                return
            return self.board[row][col]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.

        car_coordinates: List[Tuple] = car.car_coordinates()
        color = car.get_name()
        # check that no car with same color in board
        if not self._unique(color):
            return False
        # check that all coordinates are in board and empty:
        for coordinates in car.car_coordinates():
            if not self._in_board(coordinates) or self.cell_content(coordinates) != None:
                return False
        # add car to board
        for coordinate in car_coordinates:
            self._change_cell_on_board(coordinate, color)
        self.cars_on_board[car.get_name()] = car
        return True

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """

        new_cell: List[Tuple] = [
            item for item in self.possible_moves() if item[0] == name and item[1] == move_key]
        if new_cell == []:
            return False
        new_cell: Tuple = new_cell[0][2].split()[3:5]
        new_cell = eval(new_cell[0] + new_cell[1])
        row, col = new_cell
        if not self.cell_content(new_cell):
            self._change_cell_on_board(new_cell, name)
            car = self.cars_on_board[name]
            new_row, new_col = car.location
            if move_key in 'dr':
                self._change_cell_on_board(car.location, 'E')
                if move_key == 'd':
                    car.move('d')
            #         car.location = (new_row + 1, new_col)
                if move_key == "r":
                    #         car.location = (new_row, new_col + 1)
                    car.move("r")
            if move_key == 'l':
                self._change_cell_on_board((row, col + car._Car__length), 'E')
                car.move("l")
                #     car.location = (new_row, new_col - 1)
            if move_key == 'u':
                self._change_cell_on_board((row + car._Car__length, col), 'E')
                car.move("u")
                #     car.location = (new_row - 1, new_col)
            return True
        return False

        # implement your code and erase the "pass"

    def _change_cell_on_board(self, coordinates, name) -> None:
        row, col = coordinates
        self.board[row][col] = name
