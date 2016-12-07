import re

DIRECTIONS = [
    'N',
    'E',
    'S',
    'W'
]

class Guy(object):
    def __init__(self):
        self.direction = 'N'
        self.x = 0
        self.y = 0
        self.location_history = set()
        self.location_history.add(self.get_location())

        self.instruction_regex = re.compile('(L|R)(\d+)')

    def turn(self, direction):
        delta = 1 if direction == 'R' else -1
        current_direction_index = DIRECTIONS.index(self.direction)
        new_direction_index = (current_direction_index + delta) % len(DIRECTIONS)
        self.direction = DIRECTIONS[new_direction_index]

    def move(self, amount):
        for i in range(amount):
            if self.direction == 'N':
                self.y += 1
            elif self.direction == 'E':
                self.x += 1
            elif self.direction == 'S':
                self.y -= 1
            elif self.direction == 'W':
                self.x -= 1

            location = self.get_location()
            if location in self.location_history:
                print 'Already visited: %s - Distance: %d' % (location, self.distance())
            else:
                self.location_history.add(location)


    def execute_instruction(self, instruction):
        match = self.instruction_regex.search(instruction)
        if match:
            self.turn(match.group(1))
            self.move(int(match.group(2)))

    def feed(self, instructions):
        for instruction in instructions.split(','):
            self.execute_instruction(instruction)

    def distance(self):
        return abs(self.x) + abs(self.y)

    def get_location(self):
        return self.x, self.y


instructions = "R3, L5, R2, L2, R1, L3, R1, R3, L4, R3, L1, L1, R1, L3, R2, L3, L2, R1, R1, L1, R4, L1, L4, R3, L2, L2, R1, L1, R5, R4, R2, L5, L2, R5, R5, L2, R3, R1, R1, L3, R1, L4, L4, L190, L5, L2, R4, L5, R4, R5, L4, R1, R2, L5, R50, L2, R1, R73, R1, L2, R191, R2, L4, R1, L5, L5, R5, L3, L5, L4, R4, R5, L4, R4, R4, R5, L2, L5, R3, L4, L4, L5, R2, R2, R2, R4, L3, R4, R5, L3, R5, L2, R3, L1, R2, R2, L3, L1, R5, L3, L5, R2, R4, R1, L1, L5, R3, R2, L3, L4, L5, L1, R3, L5, L2, R2, L3, L4, L1, R1, R4, R2, R2, R4, R2, R2, L3, L3, L4, R4, L4, L4, R1, L4, L4, R1, L2, R5, R2, R3, R3, L2, L5, R3, L3, R5, L2, R3, R2, L4, L3, L1, R2, L2, L3, L5, R3, L1, L3, L4, L3"
guy = Guy()
guy.feed(instructions)
print guy.x, guy.y, guy.distance()
