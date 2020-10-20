"""
Autor: Ángel Carballo Cremades

Ironhack Data Analytics bootcamp

Week 1 mini project

Chess

"""

import os

# Type of pieces tuple
PIECES =("rook","knight","bishop","king","queen","bishop","knight","rook","pawn")
TEAM = ("White","Black")

class Piece(object):
    """Chess piece class, takes inputs type, team and position on board"""
    def __init__(self, typee, team):
        self.type = typee # Type of piece, take values fron PIECES dictionary
        self.team = team # White or Black

    def __str__(self):
        return f'{self.team[0]}{self.type}'

    def move_king_knight(self,actual_position):
        """This functions is for kings only, takes actual position on the board [row,column] and returns an array of possible moves not considering friends or foes"""
        if self.type not in ["king","knight"]:
            raise TypeError('Not "king" or "knight" piece type')

        a_r,a_c = actual_position #piece actual row and column indexes
        pos_mov = [] #array containing possible moves of piece

        if self.type == 'king':# 8 possible moves of a king.
            pos_mov = [[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0],[-1,1],[-1,-1]]

        if self.type == 'knight':# Building the 8 possible places for the knight
            pos_mov = [[-2, 1], [-2, -1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1]]

        #Possible movement array, not considering friends or foes. Conditional to avoid out of board places.
        pos_mov = [[a_r+row,a_c+column] for row,column in pos_mov if a_r+row>=0 and a_c+column>=0 and a_r+row<=7 and a_c+column<=7]
        return pos_mov

    def move_pawn(self,actual_position):
        """This functions is for pawns only, takes actual position on the board [row,column] and returns an array of possible moves not considering friends or foes"""
        if self.type != "pawn":
            raise TypeError('Not "pawn" piece type')

        a_r,a_c = actual_position #piece actual row and column indexes
        pos_mov = [] #array containing possible moves of piece

        #Checking which rows the piece can move to, preventing out of board positions
        if a_r == 0:
            rows = [0,1]
        elif a_r == 7:
            rows = [-1,0]
        else:
            rows = [-1,0,1]

        if self.team == 'White':
            columns = [1]
            if a_c == 1: # considering first pawn movement can be 2 squares
                columns.append(2)

        if self.team == 'Black':
            columns = [-1] #Blacks move in negative direction, left
            if a_c == 6: # considering first pawn movement can be 2 squares
                columns.append(-2)

        #Possible movement array, not considering friends or foes. White pawn moves +column, Black pawn moves -column.
        pos_mov = [[a_r+row,a_c+column] for row in rows for column in columns if not (row!=0 and column in [2,-2])]

        return pos_mov

    def move_queen_rook_bishop(self,actual_position):
        """This functions is for queens, bishops or rooks only, takes actual position on the board [row,column] and returns an array of possible moves not considering friends or foes"""
        if self.type not in ["queen","rook","bishop"]:
            raise TypeError('Not "queen", "rook" or "bishop" piece type')

        a_r,a_c = actual_position #piece actual row and column indexes

        # Run to get arrays of possible movements
        # print('h_p = ', [[0,i] for i in range(1,8)])
        # print('h_n = ', [[0,-i] for i in range(1,8)])
        # print('v_p = ', [[-i,0] for i in range(1,8)])
        # print('v_n = ', [[i,0] for i in range(1,8)])
        # print('d_pp = ', [[-i,i] for i in range(1,8)])
        # print('d_pn = ', [[i,-i] for i in range(1,8)])
        # print('d_np = ', [[i,i] for i in range(1,8)])
        # print('d_nn = ', [[-i,-i] for i in range(1,8)])

        # Possible movements, h:horizontal, v:vertical, d_p:diagonal+slope, d_n:diagonal-slope. aditional p and n is to indicate direction.
        # p = up or right move, n = down or left move
        h_p =  [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]]
        h_n =  [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]]
        v_p =  [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]]
        v_n =  [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]]
        d_pp =  [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]]
        d_pn =  [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]]
        d_np =  [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]]
        d_nn =  [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]

        #Possible movement array, not considering friends or foes. Conditional to avoid out of board places.
        h_p = [[a_r+row,a_c+column] for row,column in h_p if a_c+column<=7]
        h_n = [[a_r+row,a_c+column] for row,column in h_n if a_c+column>=0]
        v_p = [[a_r+row,a_c+column] for row,column in v_p if a_r+row>=0]
        v_n = [[a_r+row,a_c+column] for row,column in v_n if a_r+row<=7]
        d_pp = [[a_r+row,a_c+column] for row,column in d_pp if a_r+row>=0 and a_c+column<=7]
        d_pn = [[a_r+row,a_c+column] for row,column in d_pn if a_c+column>=0 and a_r+row<=7]
        d_np = [[a_r+row,a_c+column] for row,column in d_np if a_r+row<=7 and a_c+column<=7]
        d_nn = [[a_r+row,a_c+column] for row,column in d_nn if a_r+row>=0 and a_c+column>=0]

        # Returning possible movements for each type of piece
        if self.type == 'queen':
            return [h_p,h_n,v_p,v_n,d_pp,d_pn,d_np,d_nn]
        elif self.type == 'rook':
            return [h_p,h_n,v_p,v_n]
        elif self.type == 'bishop':
            return [d_pp,d_pn,d_np,d_nn]


    def possible_moves(self, actual_position:list, board):
        """This function returns the positions the piece can be moved to, uses possible moves of move_* functions (board borders), allies and enemies positions."""
        a_r,a_c = actual_position #piece actual row and column indexes
        board_pos_mov = [] #array containing possible moves of piece within board
        pos_mov = [] #array containing possible moves of piece within board and analyzing allies and enemies

        # Getting possible moves from moves_* methods.
        if self.type in ['king','knight']:
            board_pos_mov = self.move_king_knight(actual_position)
        elif self.type == 'pawn':
            board_pos_mov = self.move_pawn(actual_position)
        # elif self.type == 'knight':
        #     board_pos_mov = self.move_knight(actual_position)
        elif self.type in ['queen','rook','bishop']:
            board_pos_mov = self.move_queen_rook_bishop(actual_position)

        # Analyzing possible moves with friends and foes for pawn
        if self.type == 'pawn':
            for row,column in board_pos_mov:

                # Checking for moves in horizontal direction
                if row == a_r:
                    if board[row][column] == None: #Checking for empty square
                        pos_mov.append([row,column])
                    else:
                        pass # if there is a piece in the square the pawn cannot be moved

                # Checking for moves in diagonal (attacks)
                else:
                    if board[row][column] != None: #Checking if there is a piece in the square
                        if board[row][column].team != self.team: # Checking wether the piece is ally or enemy
                            pos_mov.append([row,column]) # Append if it is enemy
                        else:
                            pass # If the piece is an ally the piece cannot be moved

        # Analyzing possible moves with friends and foes for king and knight
        if self.type in ['king','knight']:
            for row,column in board_pos_mov:
                if board[row][column] == None: #Checking for empty square
                    pos_mov.append([row,column])
                elif board[row][column].team != self.team: #Checking for ally or enemy
                    pos_mov.append([row,column])
                else:
                    pass
        # Analyzing possible moves with friends and foes for queen, rook and bishop
        elif self.type in ['queen','rook','bishop']:
            for direction in board_pos_mov: # testing for every movement direction
                for row,column in direction:
                    if type(board[row][column]) == type(self): # checking if there is a piece in the square
                        if board[row][column].team != self.team: # checking piece's team
                            pos_mov.append([row,column])
                            break # Movement stops because there is a enemy
                        else:
                            break # if the piece in the square is an ally the analyzed piece cannot move further in that direction

                    else:
                        pos_mov.append([row,column]) # If the square is empty (None) the piece can move in that direction

        return pos_mov


class Board(object):
    """Chess board class, when instantiated creates a brand new board with all pieces at start position"""
    def __init__(self):
        self.board = [[None for place in range(4)] for row in range(8)]
        # Creating white pieces, 2 rows
        self.whites = []
        self.blacks = []

        # Creating initial white and black pieces, _low are pieces from rook to rook, _high are pawns
        w_low = [Piece(PIECES[i],TEAM[0]) for i in range(8)]
        w_high = [Piece(PIECES[-1],TEAM[0]) for i in range(8)]
        b_low = [Piece(PIECES[i],TEAM[1]) for i in range(8)]
        b_high = [Piece(PIECES[-1],TEAM[1]) for i in range(8)]

        # Adding white and black pieces to board in initial positions
        for i in range(8):
            self.board[i].insert(0,w_low[i])
            self.board[i].insert(1,w_high[i])
            self.board[i].insert(6,b_high[i])
            self.board[i].insert(7,b_low[i])

        # self.whites.append(w_low)
        # self.whites.append(w_high)
        # self.blacks.append(b_low)
        # self.blacks.append(b_high)

    def __str__(self):
        # header = '\t0\t\t1\t\t2\t\t3\t\t4\t\t5\t\t6\t\t7'
        header = '\t0\t1\t2\t3\t4\t5\t6\t7'

        print(header)
        l = 'ABCDEFGH'
        r = 0
        for row in self.board:
            print('    ',l[r], end = '\t')
            for piece in row:
                print(piece, end = '\t')
            print(' ',l[r])
            r+=1
        print(header)
        return ""

    def kill_piece(self,position:list,killed=True):
        """This method kills a piece located at the position [row,column]. Board location becomes None"""
        r,c = position
        if self.board[r][c] != None: #Checking if square is empty
            if killed:
                print(f'{self.board[r][c].team} {self.board[r][c]} at {r},{c} killed')
            self.board[r][c] = None
        else:
            raise Exception("The indicated position is empty (None)")


    def move_piece(self,actual_position:list,new_position:list):
        """Changes a piece location to the one indicated, must be a valid position"""
        a_r,a_c = actual_position
        n_r,n_c = new_position

        print(f'{self.board[a_r][a_c].team} {self.board[a_r][a_c]} moved to {n_r},{n_c}')

        if self.board[n_r][n_c] != None: #If there's an enemy, kill it
            self.kill_piece([n_r,n_c])

        self.board[n_r][n_c] = self.board[a_r][a_c]
        self.kill_piece([a_r,a_c],False)

    def check_pawn(self,position):
        """This function checks wether a pawn has crossed the board and changes its type"""
        r,c = position

        if self.board[r][c].type == 'pawn' and c in [0,7]:
            print(f'\n    A {self.board[r][c].team} pawn has crossed the board!!\nIt can be promoted to queen, knight, rook or bishop.')
            while True:
                new_type = input('Chose a promotion: ')
                if new_type in ["queen","bishop","knight","rook"]:
                    self.board[r][c].type = new_type
                    break
                else:
                    clear()
                    print(self)
                    print('Please enter a valid promotion.')
        else:
            pass


def clear():
    os.system('cls')

def coordinates(player_input):
    if len(player_input) != 2: # Validating for 2 coordinates
        return None,None

    a,b = player_input
    l = 'ABCDEFGH' #accepted letters
    r = 0 #row
    c = 0 #column


    if a.isdigit():
        if int(a)<8: #valid column less than eight
            c = int(a)
        else:
            return None,None

        if b.isalpha():
            if b.upper() in l: # coordinate is a valid letter?
                r = l.index(b.upper())
            else:
                return None,None
        else: #runs if there is no letter
            return None,None

    elif b.isdigit():
        if int(b)<8: #valid column less than eight
            c = int(b)
        else:
            return None,None

        if a.isalpha():
            if a.upper() in l: # coordinate is a valid letter?
                r = l.index(a.upper())
            else:
                return None,None
        else: #runs if there is no letter
            return None,None

    else: # runs if neither a nor b are numbers
        return None,None

    return r,c

def check_win(board):
    """This function checks wether the game has ended by looking for the kings, if there is only one: True is returned, if both are alive: False is returned"""
    number_of_kings = 0
    for row in board:
        for piece in row:
            if type(piece) != type(None):
                if piece.type == 'king':
                    number_of_kings +=1

    return False if number_of_kings == 2 else True

"""GAME BEGINS"""

clear() #clear output
board = Board()


# Game intro
print("""
    HELLO TO CHESS BY ANGEL, THIS IS THE PROJECT FROM WEEK 1.

    RULES ARE LIKE CLASSIC CHESS BUT CASTLING IS NOT ALLOWED.

    YOU WILL BE ASKED TO ENTER THE COORDINATES OF LOCATIONS (LETTER-NUMBER ---> a1)
    TO CHOOSE PIECES TO BE MOVED AND SQUARES TO MOVE THEM TO.
    WHITE PIECES START WITH 'W' AND BLACK PIECES WITH 'B'\n""")

print(board)

print("""
    IF A PAWN GETS TO THE ENEMIES' FIRST ROW IT CAN BECOME ANY PIECE (EXCEPT KING...)

    THE GAME ENDS WHEN A KING IS KILLED

    GOOD LUCK!!!""")

input('(press enter to continue)')
# End of game intro


winner = ''
l = 'ABCDEFGH'
playing = True

# MAIN GAME LOOP
while playing:

    clear()
    print(board)
    print('Whites turn...')

    while True: # White loop

        print("Choose the piece you want to move.")
        white_piece = input("Piece's coordinates: ")
        r,c = coordinates(white_piece) # checking for valid input.

        # conditionals checking valid coordinates: inside board, non-empty square, White piece, and able-to-move piece
        if [r,c] == [None,None]: # If coordinate is not valid
            clear()
            print(board)
            print('Whites turn...')
            print('Please type a valid coordinate, a row (letter) and a column (number) inside the board.')
            print('Example: a1 or 1a.')
            continue

        if type(board.board[r][c]) != type(Piece('rook','White')): # if an empty square is chosen
            clear()
            print(board)
            print('Whites turn...')
            print('Please choose a coordinate with a piece.')
            continue

        elif board.board[r][c].team != 'White': # if a black piece is selected
            clear()
            print(board)
            print('Whites turn...')
            print('Please choose a coordinate with a White piece.')
            continue

        #Chosen piece's possible movements
        pos_mov = board.board[r][c].possible_moves([r,c],board.board)

        if len(pos_mov) == 0: # Checking wether there are possible moves for the chosen piece
            clear()
            print(board)
            print('Whites turn...')
            print('Please choose a piece that can be moved.')
            continue

        clear()
        print(board)

        while True: #Once a valid piece is chosen it can't be changed, movement decision loop
            print(f'Where do you want to move your {board.board[r][c].type} in {white_piece} to?')

            white_move = input("")
            r_n,c_n = coordinates(white_move) # checking for valid input.

            if [r_n,c_n] not in pos_mov:
                clear()
                print(board)
                print(f'{white_move} is not a valid movement, valid movements are:')
                print([[l[row],column] for row,column in pos_mov])
                continue

            break

        clear()
        board.move_piece([r,c],[r_n,c_n]) #Moving piece to desired location
        break

    board.check_pawn([r_n,c_n])#Is the pawn at the enemy's end?? type can be changed to other
    print(board)
    if check_win(board.board):
        winner = 'WHITE'
        break

    print('Blacks turn...')

    while True: # Black loop

        print("Choose the piece you want to move.")
        black_piece = input("Piece's coordinates: ")
        r,c = coordinates(black_piece) # checking for valid input.

        # conditionals checking valid coordinates: inside board, non-empty square, Black piece, and able-to-move piece
        if [r,c] == [None,None]: # If coordinate is not valid
            clear()
            print(board)
            print('Blacks turn...')
            print('Please type a valid coordinate, a row (letter) and a column (number) inside the board.')
            print('Example: a1 or 1a.')
            continue

        if type(board.board[r][c]) != type(Piece('rook','Black')): # if an empty square is chosen
            clear()
            print(board)
            print('Blacks turn...')
            print('Please choose a coordinate with a piece.')
            continue

        elif board.board[r][c].team != 'Black': # if a black piece is selected
            clear()
            print(board)
            print('Blacks turn...')
            print('Please choose a coordinate with a Black piece.')
            continue

        #Chosen piece's possible movements
        pos_mov = board.board[r][c].possible_moves([r,c],board.board)

        if len(pos_mov) == 0: # Checking wether there are possible moves for the chosen piece
            clear()
            print(board)
            print('Blacks turn...')
            print('Please choose a piece that can be moved.')
            continue

        clear()
        print(board)

        while True: #Once a valid piece is chosen it can't be changed, movement decision loop
            print(f'Where do you want to move your {board.board[r][c].type} in {black_piece} to?')

            black_move = input("")
            r_n,c_n = coordinates(black_move) # checking for valid input.

            if [r_n,c_n] not in pos_mov:
                clear()
                print(board)
                print(f'{black_move} is not a valid movement, valid movements are:')
                print([[l[row],column] for row,column in pos_mov])
                continue

            break

        clear()
        board.move_piece([r,c],[r_n,c_n]) #Moving piece to desired location
        break

    board.check_pawn([r_n,c_n])#Is the pawn at the enemy's end?? type can be changed to other
    print(board)
    if check_win(board.board):
        winner = 'BLACK'
        break

clear()
print(board)
print(f'THE GAME HAS ENDED!! {winner} TEAM HAS WON!!\n\n\n')
print("Thank you for playing :)")