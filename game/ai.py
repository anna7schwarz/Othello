import copy
import datetime
import sys

__author__ = 'bengt'

from game.settings import *
import sys

class AlphaBetaPruner(object):
    """Alpha-Beta Pruning algorithm."""

    inf = sys.maxsize

    def __init__(self, depth, pieces):
        self.board = 0
        self.move = 1
        self.white = 2
        self.black = 3
        self.depth = depth
        self.first_player = self.black
        self.state = self.make_state(pieces)

    def make_state(self, pieces):
        """ Returns a tuple in the form of "current_state", that is: (current_player, state).
        """
        results = {BOARD: self.board, MOVE: self.board, WHITE: self.white, BLACK: self.black}
        return self.first_player, [results[p.get_state()] for p in pieces]


    def startAlphaBeta(self):
        #print( self.state)
        validMoves = self.actions(self.state)
        moveValues = []
        for move in validMoves:
            #print (self.next_state(self.state, move))
            moveValues.append(self.alphabeta(self.next_state(self.state, move), self.depth, -AlphaBetaPruner.inf, AlphaBetaPruner.inf, False))

        return validMoves[max(enumerate(moveValues), key = lambda x: x[1])[0]]


    def alphabeta(self, state, depth, alpha, beta,maxPlayer):
        '''
        fn = lambda action: self.min_value(depth, self.next_state(self.state, action), -self.infinity,
                                           self.infinity)
        maxfn = lambda value: value[0]
        actions = self.actions(self.state)
        moves = [(fn(action), action) for action in actions]

        '''

        validMoves = self.actions(state)
        if (depth == 0 or len(validMoves) == 0):
            return self.heuristic(state)

        if (maxPlayer):
            value = -AlphaBetaPruner.inf
            for move in validMoves:
                value = max(value, self.alphabeta(self.next_state(state, move), depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if (alpha >= beta):
                    break
            return value
        else:
            value = AlphaBetaPruner.inf
            for move in validMoves:
                value = min(value, self.alphabeta(self.next_state(state, move), depth-1, alpha, beta, True))
                beta = min(beta, value)
                if (alpha >= beta):
                    break
            return value


    def heuristic(self, state):
        weights = [4, -3, 2, 2, 2, 2, -3, 4, -3, -4, -1, -1,-1, -1, -4, -3, 2, -1, 1, 0, 0, 1, -1, 2, 2, -1, 0, 1, 1, 0, -1 , 2,  2, -1, 0, 1, 1, 0, -1 , 2, 2, -1, 1, 0, 0, 1, -1, 2,  -3, -4, -1, -1,-1, -1, -4, -3, 4, -3, 2, 2, 2, 2, -3, 4]

        '''
        1. Number of Coins
        2. Mobility
        3. Corners = Good
        4. Stabillity aka each coins possibility of capture
        '''
        player = self.first_player
        _, state = state
        #player, state = state
        opponent = self.opponent(player)

        #1st heuristic Num coins
        player_pieces, opp_pieces = 0, 0
        player_weight, opp_weight = 0, 0
        opponent_pieces = 0
        #count 
        for i in range(len(state)):
            piece = state[i]
            loc_weight = weights[i]
        for piece in state:
            if (piece == player):
                player_pieces += 1
                player_weight += loc_weight
            elif(piece == opponent):
                opp_pieces += 1
                opp_weight += loc_weight
        '''print(player_pieces)
        print(opp_pieces)
        print(state)
        print(player)
        print(opponent)'''
        heu_1 = 100 * (player_pieces - opp_pieces) / float(player_pieces + opp_pieces)

        #2nd heuristic Mobility
        player_moves = len(self.get_moves(player, opponent, state))
        opp_moves = len(self.get_moves(opponent, player,state))
        if (player_moves + opp_moves > 0):
            heu_2 = 100 * ( player_moves - opp_moves) / float(player_moves + opp_moves)
        else:
            heu_2 = 0
        
        #3rd heuristic Corners
        corners = [0, 7, 56, 63]
        player_corn, opp_corn = 0, 0
        for corn in corners:
            if (state[corn] == player):
                player_corn += 1
            elif(state[corn] == opponent):
                opp_corn += 1

        if (player_corn + opp_corn > 0):
            heu_3 = 100 * (player_corn - opp_corn) / float(player_corn + opp_corn)
        else:
            heu_3 = 0

        #4 stability aka static weights
        #weights calculated above
        if (player_weight + opp_weight > 0):
            heu_4 = 100*(player_weight - opp_weight) / float(player_weight + opp_weight)

        #change weighting
        return 25* heu_1 + 5 * heu_2 + 30 * heu_3 + 25 * heu_4



    def actions(self, current_state):
        """ Returns a list of tuples as coordinates for the valid moves for the current player.
        """
        tmp_state = copy.deepcopy(current_state)
        player, state = tmp_state
        return self.get_moves(player, self.opponent(player), state)

    def opponent(self, player):
        """ Returns the opponent of the specified player.
        """
        #return self.white
        return self.white if player is self.black else self.black

    def next_state(self, current_state, action):
        """ Returns the next state in the form of a "current_state" tuple, (current_player, state).
        """
        placed   = action[0] + (action[1] * WIDTH)
        player   = copy.copy(current_state[0])
        state    = copy.copy(current_state[1])
        opponent = self.opponent(player)

        state[placed] = player
        for d in DIRECTIONS:
            if outside_board(placed, d):
                continue

            to_flip = []
            tile = placed + d
            while state[tile] == opponent and not outside_board(tile, d):
                to_flip.append(tile)
                tile += d

            if state[tile] == player:
                for piece in to_flip:
                    state[piece] = player

        return opponent, state

    def get_moves(self, player, opponent, state):
        """ Returns a generator of (x,y) coordinates.
        """
        moves = [self.mark_move(player, opponent, tile, state, d)
                 for tile in range(WIDTH * HEIGHT)
                 for d in DIRECTIONS
                 if not outside_board(tile, d) and state[tile] == player]

        return [(x, y) for found, x, y, tile in moves if found]


    def mark_move(self, player, opponent, tile, pieces, direction):
        """ Returns True whether the current tile piece is a move for the current player,
            otherwise it returns False.
        """
        if not outside_board(tile, direction):
            tile += direction
        else:
            return False, int(tile % WIDTH), int(tile / HEIGHT), tile

        if pieces[tile] == opponent:
            while pieces[tile] == opponent:
                if outside_board(tile, direction):
                    break
                else:
                    tile += direction

            if pieces[tile] == self.board:
                return True, int(tile % WIDTH), int(tile / HEIGHT), tile

        return False, int(tile % WIDTH), int(tile / HEIGHT), tile
