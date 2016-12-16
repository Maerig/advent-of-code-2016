def possible_moves(state):
    elevator_floor, floors = state

    moves = set()

    possible_deltas = []
    if elevator_floor > 0:
        possible_deltas.append(-1)
    if elevator_floor < len(floors) - 1:
        possible_deltas.append(1)

    microchips, generators = floors[elevator_floor]

    for possible_delta in possible_deltas:
        for i in xrange(len(microchips)):
            curr_microchip = microchips[i]
            moves.add((possible_delta, (curr_microchip,), ()))

            for j in xrange(i + 1, len(microchips)):
                moves.add((possible_delta, (curr_microchip, microchips[j]), ()))

            for generator in generators:
                moves.add((possible_delta, (curr_microchip,), (generator,)))

        for i in xrange(len(generators)):
            curr_generator = generators[i]
            moves.add((possible_delta, (), (curr_generator,)))

            for j in xrange(i + 1, len(generators)):
                moves.add((possible_delta, (), (curr_generator, generators[j])))

    return moves


def move_out(floor, microchips, generators):
    return (
        tuple(sorted(
            microchip
            for microchip in floor[0]
            if microchip not in microchips
        )),
        tuple(sorted(
            generator
            for generator in floor[1]
            if generator not in generators
        ))
    )


def move_in(floor, microchips, generators):
    return (
        tuple(sorted(floor[0] + microchips)),
        tuple(sorted(floor[1] + generators))
    )


def move(state, move_params):
    old_elevator_floor = state[0]
    new_elevator_floor = old_elevator_floor + move_params[0]
    microchips = move_params[1]
    generators = move_params[2]

    new_floors = []
    for i, floor in enumerate(state[1]):
        if i == old_elevator_floor:
            new_floors.append(move_out(floor, microchips, generators))
        elif i == new_elevator_floor:
            new_floors.append(move_in(floor, microchips, generators))
        else:
            new_floors.append(floor)

    return new_elevator_floor, tuple(new_floors)


def is_valid_floor(floor):
    generators = floor[1]

    if not generators:
        return True

    for microchip in floor[0]:
        if microchip not in generators:
            return False

    return True


def is_valid_state(state):
    for floor in state[1]:
        if not is_valid_floor(floor):
            return False

    return True


def is_solved(state):
    floors = state[1]

    for i in xrange(0, len(floors) - 1):
        floor = floors[i]
        if floor[0] or floor[1]:
            return False

    return True


def solve(initial_state):
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
            for possible_move in possible_moves(curr_state):
                new_state = move(curr_state, possible_move)
                if is_valid_state(new_state) and new_state not in state_history:
                    if is_solved(new_state):
                        return depth + 1

                    next_states.add(new_state)
                    state_history.add(new_state)

        print "Valid moves: %d" % len(next_states)
        curr_states = next_states
        depth += 1


building = (
    0,
    (
        (
            ('Co', 'Ru', 'Tm'),
            ('Co', 'Pm', 'Po', 'Ru', 'Tm')
        ),
        (
            ('Pm', 'Po'),
            ()
        ),
        (
            (),
            ()
        ),
        (
            (),
            ()
        )
    )
)


print building
print solve(building)
