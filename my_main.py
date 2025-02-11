# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np


size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not(self.player_X_starts)
        self.player_X_turns= self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))
        

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0]-symbol_size,grid_position[1]-symbol_size,grid_position[0]+symbol_size,grid_position[1]+symbol_size,width = symbol_thickness,outline=symbol_O_color)

    
    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)

        self.canvas.create_line(grid_position[0]-symbol_size,grid_position[1]-symbol_size,
                                grid_position[0]+symbol_size,grid_position[1]+symbol_size,
                                width=symbol_thickness,fill=symbol_X_color)
        
        self.canvas.create_line(grid_position[0]+symbol_size,grid_position[1]-symbol_size,
                                grid_position[0]-symbol_size,grid_position[1]+symbol_size,
                                width=symbol_thickness,fill=symbol_X_color)


    def display_gameover(self):
        if self.X_wins:
            self.X_score+=1
            text = "Player 1 wins"
            cool_text = "gg pd"
            color = symbol_X_color
        elif self.O_wins:
            self.O_score+=1
            text = "Player 2 wins"
            cool_text = "gg pd"
            color = symbol_O_color
        else:
            self.tie_score+=1
            text = "It's a tie"
            cool_text = ""
            color = "gray"

        self.canvas.delete("all")

        self.canvas.create_text(size_of_board/2,size_of_board/3,font =  ('Helvetica', '50'),text = text, fill = color)
        self.canvas.create_text(100,165,angle=30,text=cool_text,font=("Times","25"),fill = "blue")

        self.canvas.create_text(size_of_board/2,size_of_board*2/3,font = ("Times","30") ,text = "Scores:\n", fill = "green")
        
        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie: ' + str(self.tie_score)
        self.canvas.create_text(size_of_board/2,3*size_of_board/4,font = ("Times","20") ,text = score_text, fill = "green")
        score_text = "Click to play again\n"
        self.canvas.create_text(size_of_board/2,11*size_of_board/12,font = ("Times","15") ,text = score_text, fill = "gray")
        
        self.reset_board = True





    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position= np.array(logical_position)
        return (size_of_board/3)*logical_position+(size_of_board/6)
        
    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position//(size_of_board/3),dtype = int)
        

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True
    def is_winner(self, player):
        player = -1 if player == 'X' else 1
    
        # 3 in a row
        for i in range(3):
            if self.board_status[i][0]==self.board_status[i][1]==self.board_status[i][2] == player:
                return True
            elif self.board_status[0][i]==self.board_status[1][i]==self.board_status[2][i] == player:
                return True
        # diagonals
        for i in range(3):
            if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
                return True
            elif self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
                return True
        
        return False

    
        

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie
    
    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X') #True or False
        if not self.X_wins:
            self.O_wins = self.is_winner('O') #True or False

        if not self.O_wins:
            self.tie = self.is_tie() #True or False

        gameover = self.X_wins or self.O_wins or self.tie #si il y a un True => True

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover





    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        if not(self.reset_board):
            if self.player_X_turns:
                if not(self.is_grid_occupied(logical_position)):
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.draw_X(logical_position)
                    self.player_X_turns=not(self.player_X_turns)
            else:
                if not(self.is_grid_occupied(logical_position)):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not(self.player_X_turns)
            #Check if its gameover
            if self.is_gameover():
                self.display_gameover()
        else:#Play again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

game_instance = Tic_Tac_Toe()
game_instance.mainloop()