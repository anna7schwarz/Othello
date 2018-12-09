import os
from collections import deque
from game.board import Board
from game.controllers import PlayerController, AiController
#Moahammad start
from testAI.controllers import testAiController
import time
#Moahmmad end
from game.random_controller import RandomController
from game.settings import *

__author__ = 'bengt'


class Game(object):
    """Game ties everything together. It has a board,
    two controllers, and can draw to the screen."""
#Mohammad start
####    def __init__(self, timeout=1,
####                 display_moves=True,
####                 players=['ai', 'ai'],
####                 colour=False):
####
    def __init__(self,logmoves,logpath,showboard,depth,result_path, timeout=1,
                 display_moves=True,
                 players=['ai', 'ai'],
                 colour=False):
        self.depth = depth
        self.result_path = result_path
        self.showboard = showboard
        self.logmoves = logmoves
        self.logpath = logpath
#Mohammad end
        self.board = Board(colour)
        self.timeout = timeout
        self.ai_counter = 0
        self.list_of_colours = [BLACK, WHITE]
        self.players = players
        self.display_moves = display_moves
        self.controllers = deque([self._make_controller(c, p) for c, p in zip(self.list_of_colours, self.players)])
        self.player = self.controllers[0].get_colour()
        self.board.set_black(4, 3)
        self.board.set_black(3, 4)
        self.board.set_white(4, 4)
        self.board.set_white(3, 3)
        self.board.mark_moves(self.player)
        self.previous_move = None
        self.previous_round_passed = False

    def _make_controller(self, colour, controller_type):
        if self.showboard:
           print(colour, controller_type)
        """ Returns a controller with the specified colour.
            'player' == PlayerController,
            'ai' == AiController.
        """
        if controller_type == 'player':
            return PlayerController(self.showboard,colour)
        elif controller_type == 'random':
            return RandomController(colour)
#Mohammad start
        elif controller_type == 'testAI':
            return testAiController(self.ai_counter, colour, self.timeout)
#Mohammad end
        else:
            self.ai_counter += 1
            return AiController(self.showboard,self.ai_counter, colour, self.depth)

    def show_info(self):
        """ Prints game information to stdout.
        """
        self.player = self.controllers[0].get_colour()
        print("Playing as:       " + self.player)
        print("Displaying moves: " + str(self.display_moves))
        print("Current turn:     " + str(self.controllers[0]))
        print("Number of Black:  " + str(
            len([p for p in self.board.pieces if p.get_state() == BLACK])))
        print("Number of White:  " + str(
            len([p for p in self.board.pieces if p.get_state() == WHITE])))

    def show_board(self):
        """ Prints the current state of the board to stdout.
        """
        self.board.mark_moves(self.player)
        print(self.board.draw())

    def show_commands(self):
        """ Prints the possible moves to stdout.
        """
        moves = [self.to_board_coordinates(piece.get_position()) for piece in self.board.get_move_pieces(self.player)]
##Mohammad start
        my_moves = [self.to_my_coordinates(piece.get_position()) for piece in self.board.get_move_pieces(self.player)]
##Mohammad end
        if not moves:
            raise NoMovesError

        #print("Possible moves are: ", moves)
        print("Possible moves are: ", my_moves)
        self.board.clear_moves()

    def run(self):
        """ The game loop will print game information, the board, the possible moves, and then wait for the
            current player to make its decision before it processes it and then goes on repeating itself.
        """
        time_of_start = time.time()
        previous_move_time = time_of_start
        while True:
#Mohammad start            
            if self.showboard:
                os.system('clear')
                self.show_info()
                self.show_board()
#Moahmamd end
            try:
#Mohammad start 
                if self.showboard:
                    self.show_commands()
#Mohammad end                
                next_move = self.controllers[0].next_move(self.board)
                self.board.make_move(next_move, self.controllers[0].get_colour())
                self.previous_round_passed = False
            except NoMovesError:
                if self.previous_round_passed:
                    print("Game Over")
                    blacks = len([p for p in self.board.pieces if p.get_state() == BLACK])
                    whites = len([p for p in self.board.pieces if p.get_state() == WHITE])
#Mohammad start
                    score = blacks - whites
                    buf = "%d\n" % (score)
                    with open(self.result_path, "a") as myfile:
                        myfile.write(buf)
#Mohammad end
                    if blacks > whites:
                        print("Black won this game.")
                        exit()
                    elif blacks == whites:
                        print("This game was a tie.")
                        exit()
                    else:
                        print("White won this game.")
                        exit()
                else:
                    self.previous_round_passed = True

            self.controllers.rotate()
            if self.showboard:
               #print("Current move is: ", self.to_board_coordinates(next_move))
               print("Current move is: ", self.to_my_coordinates(next_move))
            elif str(self.controllers[0]) == "Player":
               print(self.to_my_coordinates(next_move))
            if self.logmoves:
                    with open(self.logpath, "a") as myfile:
                        myfile.write(str(self.controllers[1]) + ":\t" + self.to_my_coordinates(next_move) + "\t" + str(time.time()-time_of_start)+"\t"+str(time.time()-previous_move_time)+ "\n")
                        previous_move_time = time.time();
                        

            self.previous_move = next_move

    def to_board_coordinates(self, coordinate):
        """ Transforms an (x, y) tuple into (a-h, 1-8) tuple.
        """
        x, y = coordinate
        return '{0}{1}'.format(chr(ord('a') + x), y + 1)
#Mohammad start

    def to_my_coordinates(self, coordinate):
        """ Transforms an (x, y) tuple into (y+1, x+1) tuple.
        """
        x, y = coordinate
        return '({0},{1})'.format( y + 1,x+1)
#Mohammad end
