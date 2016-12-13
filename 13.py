MAX_WIDTH = 50
MAX_HEIGHT = 50
SEED = 1350
GOAL = (31, 39)

CELL_REP = {
    0: '?',
    1: '.',
    2: '#'
}


class Maze(object):
    def __init__(self, seed):
        self.seed = seed

        cells = []

        for x in xrange(MAX_WIDTH):
            cells.append([])
            for y in xrange(MAX_HEIGHT):
                cells[x].append(0)

        self.cells = cells

    def __repr__(self):
        rep = ""

        for y in xrange(MAX_HEIGHT):
            for x in xrange(MAX_WIDTH):
                rep += CELL_REP[self.cells[x][y]]
            rep += '\n'

        return rep

    def get_cell(self, x, y):
        if self.cells[x][y]:
            return self.cells[x][y]

        z = x * x + 3 * x + 2 * x * y + y + y * y + self.seed
        is_wall = (bin(z).count('1') % 2 == 1)
        cell_content = 2 if is_wall else 1
        self.cells[x][y] = cell_content

        return cell_content

    def movable_positions(self, x, y):
        positions = set()

        for delta_x in [-1, 1]:
            new_x = x + delta_x
            if new_x >= 0 and self.get_cell(new_x, y) == 1:
                positions.add((new_x, y))

        for delta_y in [-1, 1]:
            new_y = y + delta_y
            if new_y >= 0 and self.get_cell(x, new_y) == 1:
                positions.add((x, new_y))

        return positions


def solve(seed, part=1):
    maze = Maze(seed)
    position = (1, 1)
    maze.get_cell(*position)

    position_history = {position}
    current_pos = {position}
    depth = 0
    while True:
        print "Depth: %d" % depth
        print maze
        if not current_pos:
            return -1

        if part == 1 and GOAL in current_pos:
            return depth

        if part == 2 and depth == 50:
            return len(position_history)

        next_pos = set()
        for position in current_pos:
            movable_pos = maze.movable_positions(*position)
            next_pos |= movable_pos - position_history

        current_pos = next_pos
        position_history |= next_pos
        depth += 1

for part in [1, 2]:
    print "####### Part %d #######" % part
    print solve(SEED, part)

