# Based on https://gist.github.com/udf/20096926dafe94d53c27349fdee5f47a
import re


RE_LINE = re.compile(r'^(\w+)=(.+)$')


def int_to_hex(x):
    return '#{:08x}'.format(int(x) & 0xFFFFFFFF)


def to_signed_32bit(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000


def hex_to_int(hex_str):
    # Strip leading #
    if hex_str[0] == '#':
        hex_str = hex_str[1:]

    int_val = int(hex_str, 16)
    # Add alpha channel if it's missing
    if len(hex_str) == 6:
        int_val = int_val | 0xFF000000

    return to_signed_32bit(int_val)


def do_thing(inpath, outpath):
    lines = []
    with open(inpath) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            match = RE_LINE.match(line)
            if match:
                try:
                    line = f'{match.group(1)}={hex_to_int(match.group(2))}'
                except Exception as e:
                    raise RuntimeError('line {}: {}'.format(i, e))
            lines.append(line)

    with open(outpath, 'w', newline='\n') as f:
        f.write('\n'.join(lines))


try:
    do_thing('true_black.atthex', 'true_black.attheme')
except RuntimeError as e:
    print('Error:', e)
