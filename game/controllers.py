import datetime
import os
import queue
import threading
import sys
from game.ai import AlphaBetaPruner
from game.settings import *

__author__ = 'bengt'


class Controller(object):
    """ Interface for different types of controllers of the board
    """

    def next_move(self, pieces):
        """ Will return a single valid move as an (x, y) tuple.
        """
        pass

    def get_colour(self):
        """ Returns the colour of the controller.
        """
        pass


class PlayerController(Controller):
    """ Controller for a real, alive and kicking player.
    """

    def __init__(self, colour):
        self.colour = colour

    def next_move(self, board):
        """ Will return a single valid move as an (x, y) tuple.

            Processes input from the user, parses it, and then returns the
            chosen move if it is valid, otherwise the user can retry sending
            new input until successful.
        """
        result = None
        while result is None:
            event = input('Enter a coordinate, ex: c3, or Ctrl+D to quit: ')
            # if event[0] == '/':
            #     if event[1:] == 'quit' or event[1:] == 'q':
            #         print('Quitting. Thank you for playing.')
            #         exit()
            # else:
            try:
                if len(event) != 2:
                    raise ValueError
                x, y = event[0], event[1]
                result = self._parse_coordinates(x, y)
                found_moves = [p.get_position() for p in board.get_move_pieces(self.get_colour())]

                if not found_moves:
                    raise NoMovesError

                if result not in found_moves:
                    raise TypeError

            except (TypeError, ValueError):
                result = None
                print("Invalid coordinates, retry.")

        return result

    def get_colour(self):
        """ Returns the colour of the controller.
        """
        return self.colour

    def __str__(self):
        return "Player"

    def __repr__(self):
        return "PlayerController"

    @staticmethod
    def _parse_coordinates(x, y):
        """ Parses board coordinates into (x, y) coordinates.
        """
        return ord(x) - ord('a'), ord(y) - ord('0') - 1


stdoutmutex = threading.Lock()
workQueue = queue.Queue(1)
threads = []

class AiController(Controller):
    """ Artificial Intelligence Controller.
    """

    def __init__(self, id, colour, depth):
        self.id = id
        self.colour = colour
        self.depth = depth

    def next_move(self, board):
        #Will return a single valid move as an (x, y) tuple.
        ai = AlphaBetaPruner(self.depth, board.pieces)
        print('Thinking...')
        return ai.startAlphaBeta()
        

    def get_colour(self):
        """ Returns the colour of the controller.
        """
        return self.colour

    def __str__(self):
        return "Ai"

    def __repr__(self):
        return "AiController[" + self.id + "]"


