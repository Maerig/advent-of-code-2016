INPUT = "11110010111001001"
LENGTH = 35651584


def invert(s):
    inverted = ""

    for b in s:
        if b == '0':
            inverted += '1'
        else:
            inverted += '0'

    return inverted


def iterate(a):
    b = a[::-1]
    return a + '0' + invert(b)


def checksum(s):
    res = ""

    for i in xrange(0, len(s) - 1, 2):
        a, b = s[i:i + 2]
        res += '1' if a == b else '0'

    if len(res) % 2 == 0:
        return checksum(res)

    return res


def solve(initial_data, length):
    data = initial_data
    while len(data) < length:
        data = iterate(data)

    return checksum(data[:length])

print solve(INPUT, LENGTH)
