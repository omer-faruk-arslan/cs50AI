"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

SIZE=3

# without prunning worked and updated

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    TC: O(N)
    """
    x_count=o_count=0
    for i in range(SIZE):
        for j in range(SIZE):
            if(board[i][j]==X):
                x_count+=1
            elif(board[i][j]==O):
                o_count+=1
            
    if x_count==o_count:
        return X
    elif x_count>o_count:
        return O
    else:
        return EMPTY


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    TC: O(N)

    """
    action_set=set()

    for i in range(SIZE):
        for j in range(SIZE):
            if(board[i][j]==EMPTY):
                action_set.add((i,j))

    return action_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    TC: O(N)

    """

    copy_board=copy.deepcopy(board)
    r,c=action

    if (r<0 or r>=SIZE or c<0 or c>=SIZE) or copy_board[r][c] != EMPTY:
        raise ValueError("Invalid Move!")
    else:
        copy_board[r][c]=player(board)    

    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one (X,O) . else None
    """

    for row in range(SIZE):
        if(board[row][0]==board[row][1] and board[row][1]==board[row][2] and board[row][0]!=EMPTY):
            return board[row][0]

    for col in range(SIZE):
        if(board[0][col]==board[1][col] and board[1][col]==board[2][col] and board[0][col]!=EMPTY):
            return board[0][col]
        

    if(board[0][0]==board[1][1] and board[1][1]==board[2][2] and board[1][1]!=EMPTY):
        return board[1][1]

    if(board[0][2]==board[1][1] and board[1][1]==board[2][0] and board[1][1]!=EMPTY):
        return board[1][1]

    return None        

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    if(winner(board) is not None):
        return True
    else:
        for i in range(SIZE):
            for j in range(SIZE):
                if(board[i][j]==EMPTY):
                    return False

        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    util = 0
    win = winner(board)

    if(win is not None):
        util = 1 if win == X else -1 

    return util


def max_value(board,alpha,beta):

    if terminal(board):
        return utility(board)
    

    v = -math.inf
    for action in actions(board):
        v = max(v,min_value(result(board,action),alpha,beta))
        alpha = max(alpha,v)
        if alpha >= beta :
            break;
    return v

def min_value(board,alpha,beta):

    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        v = min(v,max_value(result(board,action),alpha,beta))
        beta = min(v,beta)
        if beta <= alpha:
            break
    return v    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # best move is the move that is worst move for oppenent when applied
    # if there are multiple best move choose any of them
    # base case : if the board is terminal the result is obvious 

    if(terminal(board)):
        return None


    current_player = player(board)

    if current_player == X:
        best_move = None
        best_val = -math.inf
        for action in actions(board):
            val = min_value(result(board,action),-math.inf,math.inf)
            if val > best_val:
                best_move = action
                best_val = val
        return best_move
    else :
        best_move = None
        best_val = math.inf
        for action in actions(board):
            val = max_value(result(board,action),-math.inf,math.inf)
            if val < best_val : 
                best_move = action
                best_val = val
        return best_move
        