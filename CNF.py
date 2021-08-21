import numpy as np
from pysat.solvers import Glucose3
import itertools

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

    res = list(map(int,res))
    return res

# get clause of a cell
def gen_clauses(k, row, col, len_of_row, len_of_col): 
    clauses = []
    temp_clause = []
    
    # p -> q :
    # 1 -> -2^-3^-4
    # -1V-2 ^ -1V-3 ^ -1V-4
    list_adj_cells = find_adj_cells(row, col, len_of_row, len_of_col)
    
    if (k == 0):
        for i in list_adj_cells:
            clauses.append([-i])
        return clauses
    elif (k == len(list_adj_cells)):
        for i in list_adj_cells:
            clauses.append([i])
        return clauses 

    # for red_cells in itertools.combinations(list_adj_cells, len(list_adj_cells) - k): # có k ô green -> có 9 - k ô red
    #     green_cells = [cell for cell in list_adj_cells if cell not in red_cells]
    #     print("cell: ", green_cells, red_cells)
    #     for cell in red_cells:
    #         temp_clause.append(-cell)
    #         for c in green_cells:
    #             temp_clause.append(-c)
    #         temp_clause.sort(reverse = True)
    #         #if temp_clause not in clauses:
    #         clauses.append(temp_clause)
    #         temp_clause = []   

    #U(k,n)= for any k+1 sqaures out of n, at least one is not true
    for u in itertools.combinations(list_adj_cells, k+1):
        for u_member in u:
            temp_clause.append(-u_member)
        clauses.append(temp_clause)
        temp_clause = []
    #L(k,n)= for any n-k+1 squares out of n, at least one is true
    for l in itertools.combinations(list_adj_cells, len(list_adj_cells)-k+1):
        for l_member in l:
            temp_clause.append(l_member)
        clauses.append(temp_clause)
        temp_clause = []
    return clauses
    
# get clause of entire board
def get_clauses(board):
    clauses = []
    for i,row in enumerate(board):
        for j,cell in enumerate(row):
            if cell != '.' :
                clauses += gen_clauses(int(cell), i, j, len(board), len(row))
                #gen_clauses_list = gen_clauses(int(cell), i, j, len(board), len(row))
                #clauses+=gen_clauses_list

    return clauses
    pass

if __name__ == '__main__':

    in_file = "input_20x30.txt"
    in_board = np.genfromtxt(in_file, delimiter=' ', dtype=str, encoding='utf8')
    print(in_board)
    clauses = get_clauses(in_board)
    print("#clause: ", len(clauses))

    # Use pysat library to solve CNFs 
    g = Glucose3()
    for it in clauses:
        g.add_clause([int(k) for k in it])
    print(g.solve())
    model = g.get_model()
    print(model)

    for i in range(len(in_board)):
        for j in range(len(in_board[0])):
            if i * len(in_board[0]) + j + 1 in model:
                print('o', end=' ')
            else:
                print('_', end=' ')
        print('')

    # Apply A* to solve CNFs