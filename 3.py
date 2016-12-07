def is_valid_triangle(a, b, c):
    return (a < b + c) and (b < a + c) and (c < a + b)


def count_valid_triangles(path):
    valid_triangles = 0

    with open(path) as f:
        for line in f:
            sides = [int(side) for side in line.split()]
            is_valid = is_valid_triangle(*sides)
            if is_valid:
                valid_triangles += 1

    return valid_triangles


def count_valid_triangles_2(path, line_length):
    valid_triangles = 0
    current_triangles = [[] for _ in range(line_length)]

    with open(path) as f:
        for line in f:
            sides = [int(side) for side in line.split()]
            for i in range(line_length):
                current_triangles[i].append(sides[i])
                if len(current_triangles[i]) == 3:
                    is_valid = is_valid_triangle(*current_triangles[i])
                    if is_valid:
                        valid_triangles += 1
                    current_triangles[i] = []

    return valid_triangles

print count_valid_triangles_2('3.txt', 3)
