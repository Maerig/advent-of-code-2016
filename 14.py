import hashlib
import re

SALT = 'ngcjuoqr'
STRETCH_COUNT = 2016

triple_regex = re.compile(r'(\w)\1{2}')
penta_regex = re.compile(r'(\w)\1{4}')


def get_hash(salt, index):
    m = hashlib.md5()
    m.update("%s%d" % (salt, index))
    return m.hexdigest()


def get_stretched_hash(salt, index):
    hashed_word = get_hash(salt, index)
    for i in xrange(STRETCH_COUNT):
        m = hashlib.md5()
        m.update(hashed_word)
        hashed_word = m.hexdigest()
    return hashed_word


def get_triplet(hashed_word):
    match = triple_regex.search(hashed_word)
    if match:
        return match.group(1)
    return None


def get_quintuplets(hashed_word):
    return penta_regex.findall(hashed_word)


def solve(salt, hash_method):
    key_count = 0

    quintuplets_list = []
    for i in xrange(999):
        quintuplets = get_quintuplets(hash_method(salt, i))
        if quintuplets:
            quintuplets_list.append((i, quintuplets))

    index = 0
    while True:
        quintuplets = get_quintuplets(hash_method(salt, index + 1000))
        if quintuplets:
            quintuplets_list.append((index + 1000, quintuplets))

        triplet = get_triplet(hash_method(salt, index))
        if triplet:
            matching_quintuplets = [
                (i, quintuplet)
                for i, quintuplet in quintuplets_list
                if index < i <= index + 1000 and triplet in quintuplet
            ]
            if matching_quintuplets:
                print "Index %d is a key" % index
                key_count += 1
                if key_count >= 64:
                    return index

        index += 1


print solve(SALT, get_hash)
print solve(SALT, get_stretched_hash)
