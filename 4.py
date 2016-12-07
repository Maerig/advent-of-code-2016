import re
import string

room_regex = re.compile("(?P<name>[a-z-]*)(?P<sector>\d+)\[(?P<checksum>[a-z]*)\]")


def parse_line(line):
    match = room_regex.match(line)
    match_dict = match.groupdict()
    return match_dict['name'], int(match_dict['sector']), match_dict['checksum']


def count_occurences(name):
    occurrences = {}
    for c in name:
        if c == '-':
            continue

        if c not in occurrences:
            occurrences[c] = 0
        occurrences[c] += 1
    return occurrences


def compute_top_five(occurrences):
    sorted_occurences = [c for c, n in sorted(occurrences.iteritems(), key=lambda (c, n): (-n, c))]
    return ''.join(sorted_occurences[:5])


def parse_file(path):
    sector_sum = 0
    with open(path) as f:
        for line in f:
            name, sector, checksum = parse_line(line)
            occurrences = count_occurences(name)
            top_five = compute_top_five(occurrences)
            if top_five == checksum:
                sector_sum += sector
                print "%s: %d" % (decrypt(name, sector), sector)
    return sector_sum


def decrypt(name, sector):
    decrypted = ""

    for c in name:
        if c == '-':
            decrypted += ' '
        elif c.lower() == c:
            decrypted += shift_letter(c, string.ascii_lowercase, sector)
        else:
            decrypted += shift_letter(c, string.ascii_uppercase, sector)

    return decrypted


def shift_letter(letter, alphabet, delta):
    letter_idx = alphabet.index(letter)
    new_idx = (letter_idx + delta) % len(alphabet)
    return alphabet[new_idx]


print parse_file('4.txt')
