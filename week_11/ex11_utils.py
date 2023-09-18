from typing import List, Tuple, Iterable, Optional, Dict, Set

Board = List[List[str]]
Path = List[Tuple[int, int]]

# def sub_in_words(word, words):
#     return any(w.lower().startswith(word.lower()) for w in words)


def make_substring_set(dictionary: Iterable[str]) -> set:
    '''create a hashable datastructure of all possible sub strings from a set of given words
    run time of O(n**3)'''
    new_set = set()
    for word in dictionary:
        new_set.add(word)
        for i in range(len(word)):
            for j in range(i+1, len(word)+1):
                new_set.add(word[i:j])
    return new_set


def in_board(board, x, y) -> bool:
    '''check that a set of given coordinates are within a given boggle board, returns True if in and False if out'''
    if x < 0 or x >= len(board) or y < 0 or y >= len(board[x]):
        return False
    return True


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    '''checks two things. 1) that path is logical path in which all tuples are connected squares.
    2) that the word is a valid word'''
    # for each tuple check that in board, and within previous tuple range
    # if valid tuple concatanate to word
    # when finished with all tuples check word
    word = ''
    previous_coor = None
    for step in path:
        # check that step is in board
        for coor in step:
            # if not in board return none
            if not 0 <= coor <= len(board) - 1:
                return
        if previous_coor:
            if not check_adj(previous_coor, step):
                return
        previous_coor = step
        # for each step, updateword
        word += board[step[0]][step[1]]
    # after iterating over all steps check if final word is in words dict
    if word in words:
        return word


def check_adj(previous_coor, coor) -> bool:
    '''checks that coordinates are adjascent to the last value in path'''
    return abs(previous_coor[0] - coor[0]) in [0, 1] and abs(previous_coor[1] - coor[1]) in [0, 1]


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''search recursively for all words in the length of n on the board'''
    result = []
    # hash data struct is O(1) in lookup
    words = set(words)
    sub_string_set = make_substring_set(words)
    # start with first square and concotanate to word
    for x in range(len(board)):
        for y in range(len(board)):
            _find_length_n_paths_helper(
                n, board, words, sub_string_set, '', x, y, [], result)
    return result


def _find_length_n_paths_helper(n: int, board: Board, words: set, sub_string_set: set, word, x, y, path, result):
    ''' from a given square search for all paths of valid words length of n that continue or begin from a
    certain square (depends on length of path).
    n: length of path
    board: boggle board
    words: iterable of words
    word: current substring consisting of the letters from the board in the current path
    x: row
    y: col
    path: list of tuple representing coordinates of steps taken so far on the board
    result: a list of paths length of n that are valid words on the board
    '''
    if not in_board(board, x, y) or (x, y) in path:
        return
    word += board[x][y]
    if word not in sub_string_set:
        word = word[:-len(board[x][y])]
        return
    path.append((x, y))
    if len(path) == n:
        if word in words:
            result.append(path[:])
        path.pop()
        word = word[:-len(board[x][y])]
        return
    for dx, dy in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
        _find_length_n_paths_helper(n, board, words, sub_string_set,
                                    word, x + dx, y + dy, path, result)
    # # after backtracking pop last addition
    # word = word[:-len(board[x][y])]
    # path.pop()


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''search recursively for all words with paths that are the length of n on the board'''
    x, y = (0, 0)
    result = []
    words = set(words)
    sub_string_set = make_substring_set(words)
    # begin searching from every square on board
    for x in range(len(board)):
        for y in range(len(board)):
            _find_length_n_words_helper(
                n, board, words, sub_string_set, '', x, y, [], result)
    return result


def _find_length_n_words_helper(n: int, board: Board, words: Iterable[str], sub_string_set: set,  word, x, y, path, result) -> None:
    ''' from a given square search for all paths of valid words length of n that continue or begin from a
    certain square (depends on length of path).
    n: length of word
    board: boggle board
    words: iterable of words
    word: current substring consisting of the letters from the board in the current path 
    x: row
    y: col
    path: list of tuple representing coordinates of steps taken so far on the board
    result: a list of paths that are valid words length of n on the board
    '''
    # check that (x, y) is on board
    if not in_board(board, x, y) or (x, y) in path:
        return
    # add current letter to word
    word += board[x][y]
    # check if word is a possible word or substring of word is in sub_string_set
    if word not in sub_string_set:
        word = word[:-len(board[x][y])]
        return
    # if possible substring then add current step to path
    path.append((x, y))
    # base case of path length of n
    if len(word) == n:
        # if good word add path to list
        if word in words:
            result.append(path[:])
        # in any case continue searching for other paths
        path.pop()
        word = word[:-len(board[x][y])]
        return
    else:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            _find_length_n_words_helper(
                n, board,  words, sub_string_set, word, x+dx, y+dy, path, result)
    path.pop()


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    '''find all possible valid paths on a given boggle board and return alist of them.
    If a word appears more then once then return higher scoring path (ie the longer path).
    The function uses a helper function to backtrack and to check all possible paths from
    each square on the board.
    params:
    board: a list of lists of chars or double chars
    words: an iterable dataset of valid words
    return a list of paths (paths are lists of tuples representing coordinates on a boggle board
    ((0,0) is the top left coordinate).'''
    paths: Dict[str, Path] = {}
    cur_path = []
    words = set(words)
    sub_string_set = make_substring_set(words)
    # search from every square on board all paths of valid words
    # that begin from there using helper function
    for x in range(len(board)):
        for y in range(len(board)):
            _max_score_paths_helper(
                board, words, sub_string_set, "", [], x, y, paths)

    result = []
    for key in paths:
        result.append(paths[key])
    return result


def _max_score_paths_helper(board: Board, words: Set[str], sub_string_set: set, word: str, path, x: int, y: int, word_paths) -> None:
    '''backtrack through board from any square on board if substring isnt the begining
    of a substring in the valid substring set.'''
    # check (x, y) in board or (x, y) already in path (path doubling back on itself)
    if not in_board(board, x, y) or (x, y) in path:
        return
    word += board[x][y]
    # base case - substring isnt begining of any word in dictionary
    if word not in sub_string_set:
        word = word[:-len(board[x][y])]
        return
    path.append((x, y))
    # if word already exists in word_path dict then compare length of path and keep longest path
    if word in word_paths and len(path) > len(word_paths[word]):
        word_paths[word] = path
    # if not in word_path dict then add
    elif word in words:
        word_paths[word] = path[:]
    # keep adding to path as long as theres a possibility of a word
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (-1, -1), (-1, 1), (1, -1)]
    for dx, dy in directions:
        _max_score_paths_helper(board, words, sub_string_set,
                                word, path, x + dx, y + dy, word_paths)
    # after backtracking pop last addition and slice word
    word = word[:-len(board[x][y])]
    path.pop()
