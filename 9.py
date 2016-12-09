def decompress_text(text):
    cursor_idx = 0
    decompressed_text = ''
    while cursor_idx < len(text):
        c = text[cursor_idx]
        if c == '(':
            marker = ''
            cursor_idx += 1
            c = text[cursor_idx]
            while c != ')':
                marker += c
                cursor_idx += 1
                c = text[cursor_idx]
            marker_params = [int(param) for param in marker.split('x')]
            cursor_idx += 1
            compressed_part = ''
            for i in xrange(marker_params[0]):
                compressed_part += text[cursor_idx]
                cursor_idx += 1
            for i in xrange(marker_params[1]):
                decompressed_text += compressed_part
        else:
            decompressed_text += c
            cursor_idx += 1
    return decompressed_text


def get_compressed_text_length(text, multiplier=1):
    cursor_idx = 0
    decompressed_length = 0
    while cursor_idx < len(text):
        c = text[cursor_idx]
        if c == '(':
            marker = ''
            cursor_idx += 1
            c = text[cursor_idx]
            while c != ')':
                marker += c
                cursor_idx += 1
                c = text[cursor_idx]
            marker_params = [int(param) for param in marker.split('x')]
            cursor_idx += 1
            compressed_part = ''
            for i in xrange(marker_params[0]):
                compressed_part += text[cursor_idx]
                cursor_idx += 1
            decompressed_length += get_compressed_text_length(compressed_part, marker_params[1])
        else:
            decompressed_length += 1
            cursor_idx += 1
    return multiplier * decompressed_length


def read_input(path):
    with open(path) as f:
        text = f.read()
    return get_compressed_text_length(text)

print read_input('9.txt')
