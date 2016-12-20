from copy import copy

MAX_VALUE = 4294967295


class Set(object):
    def __init__(self, intervals):
        self.intervals = intervals

    def __sub__(self, other_set):
        new_intervals = copy(self.intervals)

        for other_start, other_end in other_set.intervals:
            tmp_intervals = []
            for i, (own_start, own_end) in enumerate(new_intervals):
                if other_start > own_end or other_end < own_start:
                    tmp_intervals.append((own_start, own_end))
                elif other_start <= own_start and other_end < own_end:
                    tmp_intervals.append((other_end + 1, own_end))
                elif other_start > own_start and other_end < own_end:
                    tmp_intervals.append((own_start, other_start - 1))
                    tmp_intervals.append((other_end + 1, own_end))
                elif other_start > own_start and other_end >= own_end:
                    tmp_intervals.append((own_start, other_start - 1))
            new_intervals = tmp_intervals

        return Set(new_intervals)

    def __repr__(self):
        return str(self.intervals)

    def __str__(self):
        return str(self.intervals)

    def contains(self, x):
        for start, end in self.intervals:
            if start <= x <= end:
                return True
        return False

    def get_start(self):
        return min([
            start
            for start, end in self.intervals
        ])

    def get_end(self):
        return max([
            end
            for start, end in self.intervals
        ])


def solve(path):
    allowed_values = Set([(0, MAX_VALUE)])

    with open(path) as f:
        for line in f:
            start, end = [int(extremum) for extremum in line.split('-')]
            allowed_values -= Set([(start, end)])

    part_1_answer = allowed_values.get_start()
    part_2_answer = sum([
        end - start + 1
        for start, end in allowed_values.intervals
    ])
    return part_1_answer, part_2_answer

part_1_answer, part_2_answer = solve('20.txt')
print "Part 1 answer: %d" % part_1_answer
print "Part 2 answer: %d" % part_2_answer
