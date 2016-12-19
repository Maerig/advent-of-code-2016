import hashlib

OPEN = 'bcdef'
SEED = 'udskfozm'
SIZE = (4, 4)


def get_next_states(seed, path, position):
    md5_hash = hashlib.md5(seed + path).hexdigest()
    x, y = position
    next_states = []

    for md5_index, direction, new_position, can_move in [
        (0, 'U', (x, y - 1), y > 0),
        (1, 'D', (x, y + 1), y < SIZE[1] - 1),
        (2, 'L', (x - 1, y), x > 0),
        (3, 'R', (x + 1, y), x < SIZE[0] - 1)
    ]:
        if md5_hash[md5_index] in OPEN and can_move:
            next_states.append((path + direction, new_position))

    return next_states


def solve(seed):
    goal = (SIZE[0] - 1, SIZE[1] - 1)
    shortest_path = None
    longest_path_size = -1

    currents_states = [('', (0, 0))]
    while currents_states:
        next_states = [
            state
            for current_state in currents_states if current_state[1] != goal
            for state in get_next_states(seed, *current_state)
        ]
        for path, position in next_states:
            if position == goal:
                if not shortest_path:
                    shortest_path = path
                longest_path_size = len(path)
        currents_states = next_states
    return shortest_path, longest_path_size

shortest, longest_size = solve(SEED)
print "Shortest path: %s" % shortest
print "Longest path size: %d" % longest_size
