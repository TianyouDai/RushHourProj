# parses file from data directory into datastructure
#
class State:
    def __init__(self, board, blocks):
        self.board = board
        self.blocks = blocks
        self.steps = 0
        self.log = [board]

    def boardhash(self):
        h = ""
        for row in self.board:
            h += "-".join(row) + "-"
        return h

    def copyBlocksAndModify(self, new_block):
        # copy blocks dictionary use
        # new_block instead of existing
        new_blocks = {}

        for letter in self.blocks:
            b = self.blocks[letter].copy()

            # updated block
            if new_block.letter == letter:
                new_blocks[letter] = new_block

            else:
                # copy of existing block
                new_blocks[letter] = b

        return new_blocks

    def childStates(self):

        # the states reachable in one move from
        # the current state
        new_states = []

        for block in self.blocks:

            b = self.blocks[block]

            # get the two positions one space off the end of the block
            c1 = (b.coord[0] + b.p1[0], b.coord[1] + b.p1[1])
            c2 = (b.coord[0] + b.p2[0], b.coord[1] + b.p2[1])

            if check(c1[0], c1[1]) and self.board[c1[0]][c1[1]] == '#':
                # create copy of board
                new_board = [row[:] for row in self.board]

                # modify correct cells to advance the board state
                new_board[c1[0]][c1[1]] = b.letter
                new_board[b.end[0]][b.end[1]] = '#'

                # copy block and update block coords
                new_block = b.copy()

                if b.vertical: # move was up
                    new_block.setCoord((b.coord[0] - 1, b.coord[1]))
                else: # move was left
                    new_block.setCoord((b.coord[0], b.coord[1] - 1))

                # create copy of blocks with updated block
                new_blocks = self.copyBlocksAndModify(new_block)

                # create new state and update tracking parameters
                new_state = State(new_board, new_blocks)
                new_state.log = self.log[:]
                new_state.steps = self.steps + 1

                # keep log of previous board positions
                new_state.log.append(new_board)

                new_states.append(
                    new_state
                )

            if check(c2[0], c2[1]) and self.board[c2[0]][c2[1]] == '#':
                # create copy of board
                new_board = [row[:] for row in self.board]

                # modify correct cells to advance the board state
                new_board[c2[0]][c2[1]] = b.letter
                new_board[b.coord[0]][b.coord[1]] = '#'

                # copy block and modify coords
                new_block = b.copy()

                if b.vertical: # move was down
                    new_block.setCoord((b.coord[0] + 1, b.coord[1]))
                else: # move was right
                    new_block.setCoord((b.coord[0], b.coord[1] + 1))

                # create copy of blocks
                new_blocks = self.copyBlocksAndModify(new_block)

                # create new state and update tracking parameters
                new_state = State(new_board, new_blocks)
                new_state.log = self.log[:]
                new_state.steps = self.steps + 1

                # keep log of previous board positions
                new_state.log.append(new_board)

                new_states.append(
                    new_state
                )

        return new_states

    def isSolved(self):
        return self.board[2][5] == 'x'

    def print_board(self):
        _ = [print(" ".join(row).replace("#", "☐")) for row in self.board]

class Block:
    def __init__(self, coord, p1, p2, length, letter):
        self.letter = letter
        self.coord = coord # top left coord of block
        self.vertical = True if (p1[1] == p2[1]) else False
        self.length = length
        self.p1 = p1 # p1 and p2 are offset to first empty space
        self.p2 = p2 # off the end of the block

        # bottom right coord
        if self.vertical:
            self.end = (self.coord[0] + self.length - 1, self.coord[1])
        else:
            self.end = (self.coord[0], self.coord[1] + self.length - 1)

    def __eq__(self, other):
        a = self.letter == other.letter
        b = self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]
        c = self.vertical == other.vertical
        d = self.length == other.length
        e = self.p1[0] == other.p1[0] and self.p1[1] == other.p1[1]
        f = self.p2[0] == other.p2[0] and self.p2[1] == other.p2[1]
        g = self.end[0] == other.end[0] and self.end[1] == other.end[1]
        return (a and b and c and d and e and f and g)

    def setCoord(self, c1):
        d1, d2 = c1[0] - self.coord[0], c1[1] - self.coord[1]
        self.coord = c1[0], c1[1]
        self.end = self.end[0] + d1, self.end[1] + d2

    def copy(self):
        return Block(
            self.coord,
            self.p1,
            self.p2,
            self.length,
            self.letter)

    def __repr__(self):
        s = "Block: " + self.letter + "\n"
        s += "  coord: (" + str(self.coord[0]) + ", " + str(self.coord[1]) + ")\n"
        s += "  vert: " + ("True" if self.vertical else "False") + "\n"
        s += "  length: " + str(self.length) + "\n"
        s += "  p1: " + str(self.p1) + "\n"
        s += "  p2: " + str(self.p2) + "\n"
        return s

#
# main
#

# returns board and blocks representing parsed data file
def parse(level):

    # init
    board_size = 4

    # get the level number from the command line
    level_number = level

    # open the data file in data directory
    data_file = open("data/L" + str(level_number) + ".txt")

    # read in the data for the board
    board = _createBoard(data_file, board_size)

    # create instance of Block class for each block
    blocks = _createBlocks(board, board_size)

    return State(board, blocks)

def _createBoard(data_file, board_size):

    board = []

    for i in range(board_size):
        board.append(data_file.readline()[:-1].split(" "))

    return board

def _createBlocks(board, board_size):

    visited = {}
    blocks = {}

    for r in range(board_size):
        for c in range(board_size):

            # hash tag represents empty square
            if board[r][c] == '#': continue

            h = _hash(r,c)
            if not h in visited:

                visited[h] = True

                # get letter at this position
                letter = board[r][c]

                # down and left
                adj = [(1, 0), (0, 1)]

                for a in adj:

                    rr = r + a[0]
                    cc = c + a[1]
                    if check(rr, cc) and letter == board[rr][cc]:
                        visited[_hash(rr, cc)] = True

                        # length 3
                        rrr = r + a[0]*2
                        ccc = c + a[1]*2
                        if check(rrr, ccc) and letter == board[rrr][ccc]:
                            visited[_hash(rrr, ccc)] = True

                            letter = board[r][c]
                            blocks[letter] = Block(
                                    (r, c), # coordinate
                                    (-1 * a[0], -1 * a[1]), # endpoint one
                                    (3 * a[0], 3 * a[1]), # endpoint two
                                    3, # length
                                    letter
                                )

                        # length 2
                        else:
                            letter = board[r][c]
                            blocks[letter] = Block(
                                    (r, c), # coordinate
                                    (-1 * a[0], -1 * a[1]), # endpoint one
                                    (2 * a[0], 2 * a[1]), # endpoint two
                                    2, # length
                                    letter
                                )
    return blocks

# helper function
def _hash(r, c):
    return str(r) + "-" + str(c)

def check(r, c):
    board_size = 4
    return r >= 0 and r < board_size and c >= 0 and c < board_size
