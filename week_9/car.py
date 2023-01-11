from typing import *


class Car:
    """
    car objects
    """
    VALID_ORIENTATIONS: list[str] = ['u', 'd', 'l', 'r']

    def __init__(self, name, length, location, orientation) -> None:
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        # if 2 <= length <= 4:
        self.__length = length
        # for coor in location:
        #     if coor < 0:
        #         print("negative coordinates!")
        #         return
        self.location = location
        if orientation == 1 or orientation == 0:
            self.__orientation: int = orientation
        self._possible_moves = {}

    def car_coordinates(self) -> List:
        """
        :return: A list of coordinates the car is in
        """
        # implement your code and erase the "pass"
        coordinates: List[Tuple] = []
        for i in range(self.location[self.__orientation], self.location[self.__orientation] + self.__length):
            if self.__orientation == 1:
                coordinates.append((self.location[0], i))
            else:
                coordinates.append((i, self.location[1]))
        return coordinates

    def possible_moves(self) -> Dict:
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        possible_moves = {}
        # For this car type, keys are from 'udrl'

        # The keys for vertical cars are 'u' and 'd'.
        if self.__orientation == 0:
            up = self.location[0] - 1, self.location[1]
            down = self.location[0] + self.__length, self.location[1]
            # (self.location[0] - 1, self.location[1])
            possible_moves['u'] = f"move up to {up}"
            # (self.location[0] + self.__length, self.location[1])
            possible_moves['d'] = f"move down to {down}"

        # The keys for horizontal cars are 'l' and 'r'.
        if self.__orientation == 1:
            left = self.location[0], self.location[1] - 1
            right = self.location[0], self.location[1] + self.__length
            # (self.location[1] - 1, self.location[0])
            possible_moves['r'] = f"move right to {right}"
            # (self.location[1] + self.__length, self.location[0])
            possible_moves['l'] = f"move left to {left}"

        # You may choose appropriate strings.
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        self._possible_moves_dict = possible_moves
        return possible_moves

    def movement_requirements(self, move_key) -> list:
        """
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        empties: list = []
        if len(self._possible_moves_dict) != 0:
            possibles = self._possible_moves_dict
        else:
            possibles: dict = self.possible_moves() 
        if move_key in possibles:
            # get the tuple of coordinates that's in 3rd spot of string in value of move_key
            coor: Any = possibles[move_key].split()[3:5]
            coor: Any = coor[0] + coor[1]
            empties.append(eval(coor))
            return empties
        return empties

    def move(self, move_key: str) -> bool:
        """
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        method assumes any move is legal (movement validation accures in board.move_car())
        This method updates the cars location
        """
        # check that requested movement is compatable with orientation
        if self.__orientation == 0 and move_key in ['u', 'd']:
            new_loc = new_loc = self.movement_requirements(move_key)[0]
            if move_key == 'u':
                self.location = new_loc
                return True
            if move_key == 'd':
                self.location = (new_loc[0] - self.__length + 1, new_loc[1])
                return True
        if self.__orientation == 1 and move_key in ['r', 'l']:
            new_loc = new_loc = self.movement_requirements(move_key)[0]
            if move_key == 'l':
                self.location = new_loc
                return True
            if move_key == 'r':
                self.location = (new_loc[0], new_loc[1] - self.__length + 1)
                return True
        # unable to move because uncompatable movement or not a valid direction
        return False

        # implement your code and erase the "pass"

        pass

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
