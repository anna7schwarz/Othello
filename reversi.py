#!/usr/bin/env python3

import argparse
from game.game import Game


def main():
    """ Reversi game with human player vs AI player.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', help="Number of seconds the brain is allowed to think before making its move.",
                        type=int, default=1)
    parser.add_argument('--display-moves', help="Whether legal moves should be displayed or not.", action='store_true')
    parser.add_argument('--colour', help="Display the game in 256 colours.", action='store_true')
    parser.add_argument('--player', help="If you want to play against the ai", action='store_true')
    parser.add_argument('--ai', help="If you want the ais to play against each other", action='store_true')
    parser.add_argument('--verify', help="Verify AI using a random player", action='store_true')
#Mohammd start
    parser.add_argument('--test', help="Test our AI against an existing AI", action='store_true')
    parser.add_argument('--depth', help="depth of search.",
                        type=int, default=1)
    parser.add_argument('--result_path', help="path to store the result of game.",
                        type=str, default="results/res.txt")
    parser.add_argument('--showboard', help="Show the board and scores", action='store_true')
    parser.add_argument('--logmoves', help="Log the moves into the file or not", action='store_true')
    parser.add_argument('--log_path', help="path to store the log of game.",
                        type=str, default="logs/log.txt")
#Mohammad end
    args = parser.parse_args()

    if args.timeout < 0:
        exit()

    players=[]
    if args.player:
        players = ['player', 'ai']
    if args.ai:
        players = ['ai', 'ai']
#Mohammad start
    if args.test:
        players = ['ai', 'testAI']
#Mohammad end
    elif args.verify:
        players = ['ai', 'random']
    if not players:
        players = ['ai', 'player']

    game = Game(
#Mohammad start 
                logmoves=args.logmoves,
                logpath=args.log_path,
                showboard=args.showboard,
		depth=args.depth,
		result_path=args.result_path,
#Mohammad end
		timeout=args.timeout,
                display_moves=args.display_moves,
                colour=args.colour,
                players=players,
		)
    game.run()


if __name__ == "__main__":
    main()
