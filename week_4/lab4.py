COL_NUM = 5
ROW_NUM = 4
NUM_PLAYER = 2

def init_board():
    board = [COL_NUM for i in range(ROW_NUM)]
    return board

def print_board(board):
    for row in board:
        print("*" * row)
        
def is_board_empty(board):
    is_empty = True
    for row in board:
        if row != 0:
            is_empty = False
    return is_empty

def get_next_player(current_player):
    return (current_player % NUM_PLAYER) + 1
    
def check_row_number_validity(row_number):
    return row_number < ROW_NUM + 1 and row_number > 0
    
    
def check_amount_taken(board, row_number, amount_taken):
    return board[row_number - 1] >= amount_taken
    

def get_input(board):
    valid = False
    while not valid:
        user_input = input("Your turn: ")
        row , amount = user_input.split(" ")
        row = int(row)
        amount = int(amount)
        if not check_row_number_validity(row) or not check_amount_taken(board, row, amount):
            print("Try again!")
        else:
            valid = True
    return row , amount

def update_board(board, user_input):
    board[user_input[0] - 1] -= user_input[1]
    
    
def run_game():
    board = init_board()
    current_player = 1
    print_board(board)
    while not is_board_empty(board):
        cur_turn = get_input(board)
        update_board(board, cur_turn)
        print_board(board)
    print("Player " + str(current_player)+ " is the winner!")

run_game()