import re


class Disc(object):
    def __init__(self, position_count, initial_position):
        self.position_count = position_count
        self.initial_position = initial_position

    def get_position(self, t):
        return (self.initial_position + t) % self.position_count


def get_discs(path):
    disc_regex = re.compile(r'Disc #\d+ has (\d+) positions; at time=0, it is at position (\d+).')

    discs = []
    with open(path) as f:
        for line in f:
            match = disc_regex.search(line)
            if match:
                discs.append(Disc(*[int(param) for param in match.groups()]))

    return discs


def solve(path):
    discs = get_discs(path)

    t = 0
    while True:
        solved = True
        for i, disc in enumerate(discs):
            position = disc.get_position(t + i + 1)
            if position != 0:
                solved = False
                break
        if solved:
            return t

        t += 1

print solve('15.txt')
