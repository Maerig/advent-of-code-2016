import hashlib
import string
from sys import stdout


def get_hex_hash(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


def is_relevant(hex_hash):
    for i in range(0, 5):
        if hex_hash[i] != '0':
            return False
    return True


def get_password(door_id):
    i = 0
    password = ""
    while len(password) < 8:
        s = "%s%s" % (door_id, i)
        hex_hash = get_hex_hash(s)
        if is_relevant(hex_hash):
            print hex_hash
            password += hex_hash[5]
        i += 1
    return password


def print_password(password):
    stdout.write("%s \r" % ''.join(password))
    stdout.flush()


def get_password_2(door_id):
    valid_positions = set(range(8))
    password = ['.' for _ in range(8)]
    print_password(password)

    i = 0
    while '.' in password:
        s = "%s%s" % (door_id, i)
        hex_hash = get_hex_hash(s)
        if is_relevant(hex_hash) and hex_hash[5] in string.digits:
            position = int(hex_hash[5])
            if position in valid_positions:
                password[position] = hex_hash[6]
                print_password(password)
                valid_positions.remove(position)
        i += 1
    return ''.join(password)


print get_password("abbhdwsy")
print get_password_2("abbhdwsy")
