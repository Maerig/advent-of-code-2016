class Elf(object):
    def __init__(self, num):
        self.num = num
        self.next_elf = None
        self.prev_elf = None

    def get_facing_elf(self, elf_count):
        elf = self
        for i in xrange(elf_count / 2):
            elf = elf.next_elf
        return elf

    def __repr__(self):
        return str(self.num)

    def __str__(self):
        return str(self.num)


def init_elves(elf_count):
    current_elf = first_elf = Elf(1)
    for i in xrange(2, elf_count + 1):
        next_elf = Elf(i)
        current_elf.next_elf = next_elf
        next_elf.prev_elf = current_elf
        current_elf = next_elf

    current_elf.next_elf = first_elf
    first_elf.prev_elf = current_elf

    return first_elf


def remove(elf):
    elf.prev_elf.next_elf = elf.next_elf
    elf.next_elf.prev_elf = elf.prev_elf


def solve(initial_elf_count, part):
    elf_count = initial_elf_count

    current_elf = init_elves(elf_count)
    removed_elf = current_elf.next_elf if part == 1 else current_elf.get_facing_elf(elf_count)
    while True:
        remove(removed_elf)
        elf_count -= 1

        next_elf = current_elf.next_elf
        if next_elf == current_elf:
            return current_elf

        current_elf = next_elf

        if part == 1:
            removed_elf = current_elf.next_elf
        elif part == 2:
            removed_elf = removed_elf.next_elf
            if elf_count % 2 == 0:
                removed_elf = removed_elf.next_elf


for part_number in [1, 2]:
    print "Part %d: %s" % (part_number, solve(3004953, part_number))
