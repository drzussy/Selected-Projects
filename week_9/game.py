from typing import *
import car
import board
import sys
import json


VALID_DIRECTION = 'udrl'
VALID_NAMES = "YBOWGR"


class Game:
    """
    create a game object that plays Rush Hour
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.game_board: board.Board = board
        self.victory = False
        # You may assume board follows the API

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        input_message = [
            "what color to move? what direction? ", "Bad input, try again! "]
        msg = 0
        # get user input
        while True:
            print(self.game_board)
            turn = input(input_message[msg])
            if len(turn) > 0:
                if turn[0] == '!':
                    self.victory = "exit"
                    return
            if len(turn) == 3:
                if turn[0] in VALID_NAMES and turn[2] in VALID_DIRECTION:
                    # attempt to move car
                    if self.game_board.move_car(turn[0], turn[2]):
                        break
                    else:
                        msg = 1
            else:
                msg = 1

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while not self.victory:
            # play turn
            self.__single_turn()

            if self.victory == "exit":
                break
            self._check_victory()

    def _check_victory(self):
        row, col = game_board.target_location()
        if self.game_board.board[row][col] != "E":
            self.victory = True


def load_json(filename):
    '''load json file'''
    json_file = filename
    with open(json_file, 'r') as file:
        car_config = json.load(file)
    # now car_config is a dictionary equivalent to the JSON file
    return car_config


if __name__ == "__main__":
    # Your code here

    game_board = board.Board()
    # load json file
    if len(sys.argv) > 1:
        cars = load_json(sys.argv[1])
    else:
        cars = load_json("week_9\car_config.json")
    cars_dict = {}
    # add legal cars to board and make a dict simultaniously
    for car_name in cars:
        if car_name in VALID_NAMES and 2 <= cars[car_name][0] <= 4:
            cur_car_obj = car.Car(car_name,
                                  cars[car_name][0], tuple(cars[car_name][1]), cars[car_name][2])
            if game_board.add_car(cur_car_obj):
                cars_dict[car_name] = cur_car_obj
    # create game object with the board
    game = Game(game_board)
    game.play()

    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
