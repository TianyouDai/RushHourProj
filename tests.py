from parse import *

# debug
D = True

#
# This file runs unit and integration tests against
# various parts of the rushhour application
#

#
# constants
#

test_board = [['a', 'a', 'o', 'o', 'o', 'b'],
['c', '#', 'd', 'd', 'e', 'b'],
['c', '#', 'x', 'x', 'e', 'f'],
['g', 'g', 'h', 'i', 'i', 'f'],
['j', 'j', 'h', 'k', '#', '#'],
['p', 'p', 'p', 'k', '#', '#']]

test_block_i = Block(
    (3, 3),
    (0, -1),
    (0, 2),
    2,
    'i')

test_block_new_i = Block(
    (3, 2),
    (0, -1),
    (0, 2),
    2,
    'i')

#
# Tests for parse
#

state = parse("_TEST")

if state == None:
    raise Exception("parse returned 'None' and was expected to return an instance State")

if test_board != state.board:
    raise Exception("board was not parsed correctly")

if len(state.blocks) != 14:
    raise Exception("Not all blocks were parsed correctly")

if test_block_i != state.blocks["i"]:
    raise Exception("Block not parsed correctly")

#
# Tests for State class
#

hash = state.boardhash()
if hash != "a-a-o-o-o-b-c-#-d-d-e-b-c-#-x-x-e-f-g-g-h-i-i-f-j-j-h-k-#-#-p-p-p-k-#-#-":
    raise Exception("Board not hashed correctly")

new_blocks = state.copyBlocksAndModify(test_block_new_i)

for b in state.blocks:

    bb = state.blocks[b]

    if b == test_block_new_i.letter:

        if test_block_new_i == bb:
            raise Exception("Block not modifed during copy")

    elif new_blocks[b] != bb:
        raise Exception("Blocks not successfully copied")

if state.isSolved() == True:
    raise Exception("False positive found for isSolved method")

# visual test: user must inspect child states to verify accuracy
if D and False:
    print("Visual Test Start State")
    new_states = state.childStates()
    state.print_board()
    print("")
    print("Child states")
    for state in new_states:
        state.print_board()
        print("")

#
# Tests for Block class
#

# coord, p1, p2, length, letter
b1 = Block(
    (3, 3),
    (0, -1),
    (0, 2),
    2,
    'a')

b2 = Block(
    (5, 5),
    (-1, 0),
    (3, 0),
    3,
    'b')

if b1 != b1:
    raise Exception("Same blocks are not considered equal")

if b1 == b2:
    raise Exception("Different blocks are considered equal")

b3 = b1.copy()
b3.setCoord((3, 2))

if b3.coord != (3, 2):
    raise Exception("Top-right coord not modified correctly")

if b3.end != (3, 3):
    raise Exception("Bottom-right coord not modified correctly")

if b1.coord == (3,2):
    raise Exception("Copy of Block was not independent")

#
# Tests for check in parse.py
#

if not check(0, 0):
    raise Exception("Bounds check test failed")

if not check(5, 5):
    raise Exception("Bounds check test failed")

if check(7, 1):
    raise Exception("Bounds check test failed")

if check(-1, 5):
    raise Exception("Bounds check test failed")






# end
