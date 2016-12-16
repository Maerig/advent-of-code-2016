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


def canonical_representation(state):
    positions_per_symbol = {
        symbol: [0, 0]
        for symbol in ['Co', 'Dl', 'El', 'Pm', 'Po', 'Ru', 'Tm']
    }

    for i, floor in enumerate(state[1]):
        for j, components in enumerate(floor):
            for component in components:
                positions_per_symbol[component][j] = i

    return tuple(sorted(tuple(positions) for positions in positions_per_symbol.values()))


def solve(initial_state):
    state_history = [
        {canonical_representation(initial_state)},
        set(),
        set(),
        set()
    ]
    curr_states = {initial_state}

    depth = 0
    while True:
        print "Depth: %d" % depth
        print "Tree size: %d" % sum(len(floor_state_history) for floor_state_history in state_history)

        if not curr_states:
            return None

        next_states = set()

        for curr_state in curr_states:
            for possible_move in possible_moves(curr_state):
                new_state = move(curr_state, possible_move)
                new_floor = new_state[0]
                if is_valid_state(new_state):
                    canon_repr = canonical_representation(new_state)
                    if canon_repr not in state_history[new_floor]:
                        if is_solved(new_state):
                            return depth + 1

                        next_states.add(new_state)
                        state_history[new_floor].add(canon_repr)

        print "Valid moves: %d" % len(next_states)
        curr_states = next_states
        depth += 1


part_1 = (
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


part_2 = (
    0,
    (
        (
            ('Co', 'Dl', 'El', 'Ru', 'Tm'),
            ('Co', 'Dl', 'El', 'Pm', 'Po', 'Ru', 'Tm')
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


for part_initial_state in [part_1, part_2]:
    print part_initial_state
    print solve(part_initial_state)
