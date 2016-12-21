import logging
import re

swap_position_regex = re.compile(r'swap position (\d+) with position (\d+)')
swap_letters_regex = re.compile(r'swap letter (\w) with letter (\w)')
rotate_regex = re.compile(r'rotate (left|right) (\d+) steps?')
rotate_letter_regex = re.compile(r'rotate based on position of letter (\w)')
reverse_positions_regex = re.compile(r'reverse positions (\d+) through (\d+)')
move_regex = re.compile(r'move position (\d+) to position (\d+)')


def swap_positions(word, x, y):
    new_word = list(word)

    a = word[x]
    b = word[y]
    new_word[x] = b
    new_word[y] = a

    return ''.join(new_word)


def swap_letters(word, x, y):
    new_word = ''

    for c in word:
        if c == x:
            new_word += y
        elif c == y:
            new_word += x
        else:
            new_word += c

    return new_word


def rotate(word, direction, steps):
    delta = 1 if direction == 'left' else -1
    word_length = len(word)

    new_word = word
    for i in xrange(steps):
        tmp_word = ''
        for j in xrange(len(word)):
            tmp_word += new_word[(j + delta) % word_length]
        new_word = tmp_word

    return new_word


def rotate_letter(word, x):
    i = word.index(x)

    return rotate(word, 'right', 1 + i + (1 if i >= 4 else 0))


def reverse_rotate_letter(word, x):
    new_word = word

    steps = 0
    while True:
        new_word = rotate(new_word, 'left', 1)
        steps += 1

        i = new_word.index(x)
        if steps == 1 + i + (1 if i >= 4 else 0):
            return new_word


def reverse_positions(word, x, y):
    new_word = ''

    for i, c in enumerate(word):
        if x <= i <= y:
            new_word += word[x + y - i]
        else:
            new_word += c

    return new_word


def move(word, x, y):
    new_word = list(word)
    del new_word[x]
    new_word.insert(y, word[x])
    return ''.join(new_word)


def run_instruction(word, instruction):
    for regex, method in [
        (swap_position_regex, swap_positions),
        (swap_letters_regex, swap_letters),
        (rotate_regex, rotate),
        (rotate_letter_regex, rotate_letter),
        (reverse_positions_regex, reverse_positions),
        (move_regex, move)
    ]:
        match = regex.match(instruction)
        if match:
            params = [
                int(param) if param.isdigit() else param
                for param in match.groups()
            ]
            return method(word, *params)
    print "Parse error for instruction %s" % instruction


def scramble(word, path):
    scrambled_word = word

    with open(path) as f:
        for instruction in f:
            scrambled_word = run_instruction(scrambled_word, instruction)
            logging.debug("%s -> %s" % (instruction.strip(), scrambled_word))

    return scrambled_word


def run_reverse_instruction(word, instruction):
    match = swap_position_regex.match(instruction)
    if match:
        reversed_params = (int(match.group(2)), int(match.group(1)))
        return swap_positions(word, *reversed_params)

    match = swap_letters_regex.match(instruction)
    if match:
        reversed_params = (match.group(2), match.group(1))
        return swap_letters(word, *reversed_params)

    match = rotate_regex.match(instruction)
    if match:
        reversed_params = ('left' if match.group(1) == 'right' else 'right', int(match.group(2)))
        return rotate(word, *reversed_params)

    match = rotate_letter_regex.match(instruction)
    if match:
        reversed_params = (match.group(1))
        return reverse_rotate_letter(word, *reversed_params)

    match = reverse_positions_regex.match(instruction)
    if match:
        reversed_params = (int(match.group(1)), int(match.group(2)))
        return reverse_positions(word, *reversed_params)

    match = move_regex.match(instruction)
    if match:
        reversed_params = (int(match.group(2)), int(match.group(1)))
        return move(word, *reversed_params)

    print "Parse error for instruction %s" % instruction


def unscramble(word, path):
    unscrambled_word = word

    with open(path) as f:
        reversed_instructions = f.readlines()[::-1]
        for instruction in reversed_instructions:
            unscrambled_word = run_reverse_instruction(unscrambled_word, instruction)
            logging.debug("%s -> %s" % (instruction.strip(), unscrambled_word))

    return unscrambled_word


def solve(word, path):
    return scramble(word, path), unscramble(word, path)


part_1_answer, part_2_answer = solve('fbgdceah', '21.txt')
print "Part 1 answer: %s" % part_1_answer
print "Part 2 answer: %s" % part_2_answer
