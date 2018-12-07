import datetime
from game.ai import AlphaBetaPruner
import threading


class Brain(threading.Thread):
    def __init__(self, q, pieces):
        self.q = q
        self.pieces = pieces
        self.has_started = False
        threading.Thread.__init__(self)

    def run(self):
        """ Starts the Minimax algorithm with the Alpha-Beta Pruning optimization
            and puts the result in a queue once done.
        """
        pruner = AlphaBetaPruner(self.depth, self.pieces)
        result = pruner.startAlphaBeta()
        self.q.put(result)

