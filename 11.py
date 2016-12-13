from copy import deepcopy


class Floor(object):
    def __init__(self, microchips, generators):
        self.microchips = set(microchips)
        self.generators = set(generators)

    def __eq__(self, other):
        return self.microchips == other.microchips and self.generators == other.generators

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "  Microchips: %s\n  Generators: %s" % (self.microchips, self.generators)

    def is_valid(self):
        for microchip in self.microchips:
            if microchip in self.generators:
                continue
            if self.generators:
                return False

        return True

    def is_empty(self):
        return not(self.microchips or self.generators)

    def move_in(self, microchips, generators):
        for microchip in microchips:
            self.microchips.add(microchip)
        for generator in generators:
            self.generators.add(generator)

    def move_out(self, microchips, generators):
        for microchip in microchips:
            self.microchips.remove(microchip)
        for generator in generators:
            self.generators.remove(generator)


class Building(object):
    def __init__(self, floors):
        self.floors = floors
        self.elevator_floor = 0

    def __eq__(self, other):
        if self.elevator_floor != other.elevator_floor:
            return False

        for own_floor, other_floor in zip(self.floors, other.floors):
            if own_floor != other_floor:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '\n'.join([
            "[%d]%s\n%s" % (i, "<-" if self.elevator_floor == i else "", floor)
            for i, floor in reversed(list(enumerate(self.floors)))
        ])

    def is_solved(self):
        for i in xrange(len(self.floors) - 1):
            if not self.floors[i].is_empty():
                return False

        return True

    def is_valid(self):
        for floor in self.floors:
            if not floor.is_valid():
                return False

        return True

    def move(self, delta, microchips, generators):
        new_state = deepcopy(self)
        new_state.floors[new_state.elevator_floor].move_out(microchips, generators)
        new_state.elevator_floor += delta
        new_state.floors[new_state.elevator_floor].move_in(microchips, generators)
        return new_state

    def possible_moves(self):
        possible_moves = set()

        possible_deltas = []
        if self.elevator_floor > 0:
            possible_deltas.append(-1)
        if self.elevator_floor < len(self.floors) - 1:
            possible_deltas.append(1)

        current_floor = self.floors[self.elevator_floor]
        microchips = list(current_floor.microchips)
        generators = list(current_floor.generators)

        for possible_delta in possible_deltas:
            for i in xrange(len(microchips)):
                curr_microchip = microchips[i]
                possible_moves.add((possible_delta, (curr_microchip,), ()))

                for j in xrange(i + 1, len(microchips)):
                    possible_moves.add((possible_delta, (curr_microchip, microchips[j]), ()))

                for generator in generators:
                    possible_moves.add((possible_delta, (curr_microchip,), (generator,)))

            for i in xrange(len(generators)):
                curr_generator = generators[i]
                possible_moves.add((possible_delta, (), (curr_generator,)))

                for j in xrange(i + 1, len(generators)):
                    possible_moves.add((possible_delta, (), (curr_generator, generators[j])))

        return possible_moves


class StateSet(object):
    pass


def solve(initial_state):
    state_history = {
        initial_state: []
    }
    curr_states = [(initial_state, [])]

    depth = 0
    while True:
        print "Depth: %d" % depth
        print "Tree size: %d" % len(state_history.keys())

        if not curr_states:
            print "Total states: %d" % len(state_history.keys())
            for state in state_history.keys():
                print state
                print "\n\n"
            return None

        next_states = []

        for curr_state, move_history in curr_states:
            for possible_move in curr_state.possible_moves():
                new_state = curr_state.move(*possible_move)
                if new_state.is_valid() and new_state not in state_history.keys():
                    new_move_history = move_history + [possible_move]

                    if new_state.is_solved():
                        return new_move_history

                    next_states.append((new_state, new_move_history))
                    state_history[new_state] = new_move_history

        print "Valid moves: %d" % len(next_states)
        curr_states = next_states
        depth += 1


# TODO special set object for states
def solve_v2(initial_state):
    state_history = {initial_state}
    curr_states = {initial_state}

    depth = 0
    while True:
        print "Depth: %d" % depth
        print "Tree size: %d" % len(state_history)

        if not curr_states:
            return None

        next_states = set()

        for curr_state in curr_states:
            for possible_move in curr_state.possible_moves():
                new_state = curr_state.move(*possible_move)
                if new_state.is_valid() and new_state not in state_history:
                    if new_state.is_solved():
                        return depth + 1

                    next_states.add(new_state)
                    state_history.add(new_state)

        print "Valid moves: %d" % len(next_states)
        curr_states = next_states
        depth += 1


building = Building([
    Floor(
        ['thulium', 'ruthenium', 'cobalt'],
        ['polonium', 'thulium', 'promethium', 'ruthenium', 'cobalt']
    ),
    Floor(
        ['polonium', 'promethium'],
        []
    ),
    Floor(
        [],
        []
    ),
    Floor(
        [],
        []
    )
])

print building
print solve_v2(building)
