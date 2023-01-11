import helper

INP_MSGS = ["Please choose the top coordinates within the board (col = CAPITAL \
letter,row = number)  for a ship size of ", "Please choose the coordinates like \
we asked dummy (column in CAPITAL letters, row in numbers (meaning 1, 2, 3 etc),\
and not on another ship for a ship size of "
            ]
TORPEDO_MSGS = ["Bridge from gunner, coordinates for torpedo over!",
                "Sir thats beyond our gimel gimel sir! Repeat coordinates!"]
helper.SHIP_SIZES


def init_board(rows, columns):
    '''This function intitializes an empty board with the input being (rows,columns)'''
    board = []
    for i in range(rows):
        board.append([helper.WATER for i in range(columns)])
    return board


def cell_loc(name):
    '''this function recieves the users input and transforms
    the lexic coordinates into 2 numbers of a grid
    function can only receive alpha_numerical parameters'''
    user_input = []
    if len(name) < 2 or len(name) > 3:  # if name is too long
        return
    # single digit number
    if len(name) == 2 and name[0].isalpha() and helper.is_int(name[1]):
        user_input.append(int(name[1]) - 1)
        user_input.append(((int(ord(name[0].upper())) - 17)) - 48)
        return user_input[0], user_input[1]
    # double digit number
    if len(name) == 3 and name[0].isalpha() and helper.is_int(name[1:]):
        user_input.append(int(name[1:]) - 1)
        user_input.append(((int(ord(name[0].upper())) - 17)) - 48)
        return user_input[0], user_input[1]
    return  # input is not legal


def valid_ship(board, size, loc):
    '''This funcion checks if the users input is a legal move in the game 
    and that the ship placement is on hidden WATER and returns True or False'''
    if 0 <= loc[1] <= helper.NUM_COLUMNS:
        for i in range(size):
            # play_again that theres space for the ship row by row
            if not 0 <= loc[0] + i < helper.NUM_ROWS or board[loc[0] + i][loc[1]] != helper.WATER:
                return False
        else:  # theres space!
            return True
    return False  # if the loc isnt in the board


def create_player_board(rows, columns, ship_sizes):
    """initiates board and prompts player for ship locations, returns board with ships"""
    board = init_board(rows, columns)
    # print board and prompt for ships in XN format
    i = 0
    prompt = 0
    if ship_sizes == ():
        return board
    while i < len(ship_sizes):
        helper.print_board(board)
        # prompt player with MSG for loc for subs (according to ship_sizes)
        ans = helper.get_input(INP_MSGS[prompt] + str(ship_sizes[i]) + ":")
        ans = cell_loc(ans)
        if ans == None:
            prompt = 1
            continue
        if valid_ship(board, ship_sizes[i], ans):
            # update board and i + 1:
            for j in range(ship_sizes[i]):
                board[ans[0] + j][ans[1]] = helper.SHIP
            prompt = 0
            i += 1
        else:  # reprompt
            prompt = 1
    return board


def create_computer_board(rows: int, columns: int, ship_sizes: list):
    """initiates board and loops to get valid locations for computer and uses random functions to place ships"""
    board = init_board(rows, columns)
    # print board and prompt for ships in XN format
    i = 0
    while i < len(ship_sizes):
        locations = set([(s, j) for s in range(rows) for j in range(columns)
                         if valid_ship(board, ship_sizes[i], (s, j))])
        ans = helper.choose_ship_location(board, ship_sizes[i], locations)
        if valid_ship(board, ship_sizes[i], ans):
            # update board and i + 1:
            for j in range(ship_sizes[i]):
                board[ans[0] + j][ans[1]] = helper.SHIP
            i += 1
    return board


def valid_torpedo_coor(loc: tuple):
    """checks that firing coordinates are valid, returns True or False"""
    if loc == None:
        return False
    if 0 <= loc[0] <= helper.NUM_ROWS - 1 and 0 <= loc[1] <= helper.NUM_COLUMNS - 1:
        return True
    return False


def fire_torpedo(board: list, loc: tuple):
    """receives firing coordinates and if the location is valid updates and returns board"""
    if valid_torpedo_coor(loc):
        if board[loc[0]][loc[1]] == helper.SHIP or board[loc[0]][loc[1]] == helper.HIT_SHIP:
            board[loc[0]][loc[1]] = helper.HIT_SHIP
        else:
            board[loc[0]][loc[1]] = helper.HIT_WATER
    return board


def hidden_print_board(board2: list):
    """print boards while computers ships are hidden"""
    hidden_board = []
    for i in range(len(board2)):
        hidden_board.append([])
        for j in range(len(board2[i])):
            if board2[i][j] == helper.SHIP:
                hidden_board[i].append(helper.WATER)
            else:
                hidden_board[i].append(board2[i][j])
    return hidden_board


def check_win(board1: list, board2: list):
    no_hit1 = False
    no_hit2 = False
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if board1[i][j] == helper.SHIP:
                no_hit1 = True
            if board2[i][j] == helper.SHIP:
                no_hit2 = True
    # if theres a winner, exit while loop
    return no_hit1, no_hit2


def final_message_and_promt(no_hit1: bool, no_hit2: bool):
    '''prompt player acoording to who won and returns wether hed like to play again'''
    valid = False
    while not valid:  # prompt user until given a valid input
        # combine two ifs into one if with f string and winner as a variable
        if no_hit1 == False:
            play_again = helper.get_input("Computer won, better luck next time. Would you\
like to play again? ")
        elif no_hit2 == False:
            play_again = helper.get_input(
                "You won! would you like to play again? ")
        if play_again == "Y" or play_again == "N":
            valid = True
    return play_again


def create_boards(num_rows: int, num_cols: int, sizes: list):
    board1 = create_player_board(num_rows, num_cols, sizes)
    board2 = create_computer_board(num_rows, num_cols, sizes)
    return board1, board2


def get_torpedo_coordinates():
    '''prompt player for coordinates, validate them and then return them. 
    also reprompt if given bad coordinates'''
    prompt = 0
    while True:
        # prompt user for coordinates to fire
        torp = helper.get_input(TORPEDO_MSGS[prompt])
        torp = cell_loc(torp)  # transform to usable coordinate
        if valid_torpedo_coor(torp):
            prompt = 0
            break
        else:
            prompt = 1
    return torp


def main():
    while True:
        board1, board2 = create_boards(helper.NUM_ROWS, helper.NUM_COLUMNS,
                                       helper.SHIP_SIZES)
        # round of game
        game_finished = False
        while not game_finished:
            hidden_board = hidden_print_board(board2)
            helper.print_board(board1, hidden_board)

            # players turn
            turn = get_torpedo_coordinates()
            board2 = fire_torpedo(board2, turn)

            # computers turn
            locations = set([(s, j) for s in range(helper.NUM_ROWS) for
                             j in range(helper.NUM_COLUMNS) if board1[s][j] != helper.HIT_SHIP and
                             board1[s][j] != helper.HIT_WATER])
            board1 = fire_torpedo(
                board1, helper.choose_torpedo_target(hidden_board, locations))

            # check for winner
            no_hit1, no_hit2 = check_win(board1, board2)
            # if theres at least one winner, exit while loop
            if no_hit1 == False or no_hit2 == False:
                game_finished = True

        helper.print_board(board1, board2)
        play_again = final_message_and_promt(no_hit1, no_hit2)
        if play_again == "Y":
            continue
        if play_again == "N":
            break


if __name__ == "__main__":
    main()
