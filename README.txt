To run the game without printing the board with the default board configuration:
python3 reversi.py
______________________________________________________________________________________________________
To change the depth of searching in alpha beta use --depth=DEPTH
python3 reversi.py --depth=2
______________________________________________________________________________________________________
To change the init configuration of the game:
python3 reversi.py --init_board 000000000000000000000000000WB000000BW000000000000000000000000000
_____________________________________________________________________________________________________
To show the board and info while playing:
python3 reversi.py --showboard
____________________________________________________________________________________________________
To show the board in colour
python3 reversi.py --showboard --colour
___________________________________________________________________________________________________
To run against a random player add --verify
python3 reversi.py --showboard --colour --verify
__________________________________________________________________________________________________

To run against an existing AI algorithm player add --test
python3 reversi.py --showboard --colour --test
__________________________________________________________________________________________________



