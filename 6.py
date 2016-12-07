def sort_count_dict_asc(count_dict):
    return sorted(count_dict, key=lambda c: count_dict[c])


def sort_count_dict_desc(count_dict):
    return sorted(count_dict, key=lambda c: -1 * count_dict[c])


def read_lines(path, line_size, sort_method):
    col_counts = [{} for _ in range(0, line_size)]

    with open(path) as f:
        for line in f:
            for i, c in enumerate(line.strip()):
                if c not in col_counts[i]:
                    col_counts[i][c] = 0
                col_counts[i][c] += 1

    return ''.join([sort_method(col_count)[0] for col_count in col_counts])

print read_lines('6.txt', 8, sort_count_dict_asc)
