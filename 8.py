import re

rect_regex = re.compile("rect (\d+)x(\d+)")
rotate_column_regex = re.compile("rotate column x=(\d+) by (\d+)")
rotate_row_regex = re.compile("rotate row y=(\d+) by (\d+)")


class Screen(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
        for x in xrange(width):
            self.pixels.append([])
            for y in xrange(height):
                self.pixels[x].append(0)

    def rect(self, width, height):
        for x in xrange(width):
            for y in xrange(height):
                self.pixels[x][y] = 1

    def rotate_column(self, x, by):
        new_column = [0 for _ in xrange(self.height)]
        for i in xrange(by):
            for j in xrange(self.height):
                new_column[j] = self.pixels[x][j - 1]
            self.pixels[x] = new_column[:]

    def rotate_row(self, y, by):
        new_row = [0 for _ in xrange(self.width)]
        for i in xrange(by):
            for j in xrange(self.width):
                new_row[j] = self.pixels[j - 1][y]
            for j in xrange(self.width):
                self.pixels[j][y] = new_row[j]

    def count_lit_pixels(self):
        count = 0

        for x in xrange(self.width):
            for y in xrange(self.height):
                count += self.pixels[x][y]

        return count

    def __repr__(self):
        rep = ""
        for y in xrange(self.height):
            for x in xrange(self.width):
                rep += "#" if self.pixels[x][y] else "."
            rep += '\n'
        return rep


def read_lines(path):
    screen = Screen(50, 6)
    with open(path) as f:
        for line in f:
            if rect_regex.match(line):
                width, height = rect_regex.match(line).groups()
                screen.rect(int(width), int(height))
            elif rotate_column_regex.match(line):
                x, by = rotate_column_regex.match(line).groups()
                screen.rotate_column(int(x), int(by))
            elif rotate_row_regex.match(line):
                y, by = rotate_row_regex.match(line).groups()
                screen.rotate_row(int(y), int(by))
            else:
                print "Parse failed: " + line
            print screen
    return screen.count_lit_pixels()

print read_lines('8.txt')
