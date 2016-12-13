class Cpu(object):
    def __init__(self):
        self.registries = {
            'a': 0,
            'b': 0,
            'c': 1,
            'd': 0
        }
        self.ip = 0
        self.instructions = []

    def get_val(self, x):
        if x in ['a', 'b', 'c', 'd']:
            return self.registries[x]
        return int(x)

    def cpy(self, x, y):
        self.registries[y] = x
        self.ip += 1

    def inc(self, x):
        self.registries[x] += 1
        self.ip += 1

    def dec(self, x):
        self.registries[x] -= 1
        self.ip += 1

    def jnz(self, x, y):
        if x != 0:
            self.ip += y
        else:
            self.ip += 1

    def run_instruction(self, instruction):
        args = instruction.split()
        if args[0] == 'cpy':
            self.cpy(self.get_val(args[1]), args[2])
        elif args[0] == 'inc':
            self.inc(args[1])
        elif args[0] == 'dec':
            self.dec(args[1])
        elif args[0] == 'jnz':
            self.jnz(self.get_val(args[1]), self.get_val(args[2]))

    def run_instructions(self, instructions):
        self.instructions = instructions
        self.ip = 0
        while self.ip < len(self.instructions):
            self.run_instruction(self.instructions[self.ip])

with open('12.txt') as f:
    instructions = f.readlines()
cpu = Cpu()
cpu.run_instructions(instructions)
print cpu.registries
