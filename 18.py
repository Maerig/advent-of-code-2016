FIRST_ROW = ".^.^..^......^^^^^...^^^...^...^....^^.^...^.^^^^....^...^^.^^^...^^^^.^^.^.^^..^.^^^..^^^^^^.^^^..^"
ROW_COUNT = 400000


def get_tile(prev_tiles):
    if ''.join(prev_tiles) in ('^^.', '.^^', '^..', '..^'):
        return '^'
    return '.'


def get_rows(first_row):
    yield first_row

    row_length = len(first_row)
    last_row = first_row
    while True:
        next_row = ""

        for i in xrange(row_length):
            prev_tiles = tuple(
                last_row[j] if 0 <= j < row_length else '.'
                for j in (i - 1, i, i + 1)
            )
            next_row += get_tile(prev_tiles)

        yield next_row
        last_row = next_row


def solve(first_row, row_count):
    safe_tile_count = 0

    for i, row in enumerate(get_rows(first_row)):
        if i >= row_count:
            return safe_tile_count

        if row_count <= 50:
            print row
        safe_tile_count += row.count('.')

print solve(FIRST_ROW, ROW_COUNT)
