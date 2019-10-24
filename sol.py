import sys
from parse import parse

# loop until queue of states is empty
def sol():

    # parse data file to get
    # initial state
    start_state = None
    if len(sys.argv) == 2:
        start_state = parse(int(sys.argv[1]))
    else:
        start_state = parse(40)

    # queue holds game states
    q = []

    # push initial state
    q.append(start_state)

    # track visited states
    visited = {}

    # mark state as visited
    visited[start_state.boardhash()] = True

    # holds solution state
    solution = None

    while len(q) > 0:

        # get next state from queue
        # (BFS finds shortest solution)
        cur = q.pop(0)

        # check for win condition
        if False:
            if cur.isSolved():
                return cur

        # get all child states of the cur state
        new_states = cur.childStates()

        # only add child states if we have not seen them before
        for state in new_states:

            hash = state.boardhash()

            if not hash in visited:

                # mark state as visited
                visited[hash] = True

                q.append(state)

    print("Unique states", len(visited))
    return None

#
# helper functions
#

# print the board followed by the blocks
def _print_data(state):
    for row in state.board: print(row)
    print("\n")
    for letter in state.blocks:
        block = state.blocks[letter]
        print("letter:", block.letter)
        print("coord:", block.coord)
        print("vertical:", block.vertical)
        print("length:", block.length)
        print("  p1:", block.p1)
        print("  p2:", block.p2, "\n")

# print the steps that this solution contains
def _print_log(solution):

    if len(sys.argv) == 2:
        print("\nLevel " + str(sys.argv[1]) + " solution")
    else:
        print("\nLevel " + str(33) + " solution")

    _ = [print(" ".join(row).replace("#", "☐")) for row in solution.log[0]]
    print("")

    step  = 1
    steps = len(solution.log) - 1

    for board in solution.log[1:]:
        print(" STEP:", step, "of", steps)
        step += 1
        _ = [print(" ".join(row).replace("#", "☐")) for row in board]
        print("")


#
# main
#
solution = sol()
# _print_log(solution)
