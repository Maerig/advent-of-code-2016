import re

ip_regex = re.compile("(\w+)\[(\w+)\](\w+)")


def has_abba(word):
    for i in range(0, len(word) - 3):
        slice = word[i:i+4]
        if slice[0] == slice[3] and slice[1] == slice[2] and slice[0] != slice[1]:
            return True

    return False


def is_tls(address):
    has_one = False
    current_word = ''
    for c in address:
        if c == '[':
            has_one = has_one or has_abba(current_word)
            current_word = ''
        elif c == ']':
            if has_abba(current_word):
                return False
            current_word = ''
        else:
            current_word += c
    has_one = has_one or has_abba(current_word)
    return has_one


def get_abas(word):
    aba_list = []

    for i in range(0, len(word) - 2):
        slice = word[i:i+3]
        if slice[0] == slice[2] and slice[0] != slice[1]:
            aba_list.append(slice)

    return aba_list


def get_bab(aba):
    return aba[1] + aba[0] + aba[1]


def if_ssl(address):
    aba_list = []
    bab_list = []
    current_word = ''
    for c in address:
        if c == '[':
            aba_list += get_abas(current_word)
            current_word = ''
        elif c == ']':
            bab_list += get_abas(current_word)
            current_word = ''
        else:
            current_word += c

    aba_list += get_abas(current_word)

    for aba in aba_list:
        if get_bab(aba) in bab_list:
            return True

    return False


def read_lines(path):
    count = 0

    with open(path) as f:
        for line in f:
            if if_ssl(line.strip()):
                count += 1

    return count

print read_lines('7.txt')