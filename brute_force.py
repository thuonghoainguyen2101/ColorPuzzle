import numpy as np
import itertools
from sys import exit

# create a list of adj cell of input cell
def find_adj_cells(row, col, len_of_row, len_of_col): 
    res = []
    board = np.arange(start = 1, stop = len_of_row * len_of_col + 1, step = 1)
    board = np.reshape(board, (len_of_row, len_of_col))

    # corner -> 4 adj cells
    # cell is at top left corner
    if row == 0 and col == 0 :
        res.append(board[0][0])
        res.append(board[0][1])
        res.append(board[1][0])
        res.append(board[1][1])
        
    # cell is at top right corner
    elif row == 0 and col == len_of_col - 1 :
        res.append(board[0][len_of_col - 2])
        res.append(board[0][len_of_col - 1])
        res.append(board[1][len_of_col - 2])
        res.append(board[1][len_of_col - 1])
        

    # # cell is at bottom left corner
    elif row == len_of_row - 1 and col == 0 :
        res.append(board[len_of_row - 2][0])
        res.append(board[len_of_row - 1][0])
        res.append(board[len_of_row - 2][1])
        res.append(board[len_of_row - 1][1])
        
    # # cell is at bottom right corner
    elif row == len_of_row - 1 and col == len_of_col - 1 :
        res.append(board[len_of_row - 2][len_of_col - 2])
        res.append(board[len_of_row - 1][len_of_col - 2])
        res.append(board[len_of_row - 2][len_of_col - 1])
        res.append(board[len_of_row - 1][len_of_col - 1])

    # edge -> 6 adj cells
    # cell is at top edge
    elif row == 0 :
        res.append(board[0][col - 1])
        res.append(board[0][col])
        res.append(board[0][col + 1])
        res.append(board[1][col - 1])
        res.append(board[1][col])
        res.append(board[1][col + 1])

    # cell is at bottom edge
    elif row == len_of_row - 1 :
        res.append(board[row - 1][col - 1])
        res.append(board[row - 1][col])
        res.append(board[row - 1][col + 1])
        res.append(board[row][col - 1])
        res.append(board[row][col])
        res.append(board[row][col + 1])

    # cell is at left edge
    elif col == 0 :
        res.append(board[row - 1][0])
        res.append(board[row][0])
        res.append(board[row + 1][0])
        res.append(board[row - 1][1])
        res.append(board[row][1])
        res.append(board[row + 1][1])

    # cell is at right edge
    elif col == len_of_col - 1 :
        res.append(board[row - 1][col - 1])
        res.append(board[row][col - 1])
        res.append(board[row + 1][col - 1])
        res.append(board[row - 1][col])
        res.append(board[row][col])
        res.append(board[row + 1][col])

    # inside -> 9 adj cells
    else:
        res.append(board[row - 1][col - 1])
        res.append(board[row][col - 1])
        res.append(board[row + 1][col - 1])
        res.append(board[row - 1][col])
        res.append(board[row][col])
        res.append(board[row + 1][col])
        res.append(board[row - 1][col + 1])
        res.append(board[row][col + 1])
        res.append(board[row + 1][col + 1])
    return res

# check if current cell is satisfy
def check_cell(cell_value, row, col, len_of_row, len_of_col, board):
    if cell_value == '.':
        return True
    cell_value = int(cell_value)
    sum_adj = 0
    list_adj_cell = find_adj_cells(row, col, len_of_row, len_of_col)
    for i in list_adj_cell:
        sum_adj += board[i - 1]

    return sum_adj == cell_value

# check if current board is the correct answer
def check_board(in_board, out_board):
    len_of_row = len(in_board) 
    len_of_col = len(in_board[0])

    for i in range(len_of_row):
        for j in range (len_of_col):
            if not check_cell(in_board[i][j], i, j, len_of_row, len_of_col, out_board) :
                return False
    return True

if __name__ == '__main__':
    in_file = "input.txt"
    in_board = np.genfromtxt('input.txt', delimiter=' ', dtype=str, encoding='utf8')
    # Program brute-force algorithm
    len_of_row = len(in_board) 
    len_of_col = len(in_board[0])

    # for each iterable
    for out_board in itertools.product(range(2), repeat = len_of_row * len_of_col):
        # check if current iterable is correct
        if check_board(in_board, out_board):
            out_board.reshape(len_of_row, len_of_col)
            print("res: ", out_board)
            exit()
    print("Problem cant be solved")