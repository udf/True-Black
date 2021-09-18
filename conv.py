# usage python theme_conv.py file.[atthex|attheme]

import sys
from os import path
import re


RE_LINE = re.compile(r'^(\w+)=(.+)$')


def int_to_hex(x):
    return '#{:08x}'.format(int(x) & 0xFFFFFFFF)


def to_signed_32bit(n):
    n = n & 0xffffffff
    return (n ^ 0x80000000) - 0x80000000


def hex_to_int(x):
    if x[0] == '#':
        x = x[1:]
    return to_signed_32bit(int(x, 16))


def do_thing(inpath, outpath, converter):
    lines = []
    with open(inpath) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            match = RE_LINE.match(line)
            if match:
                try:
                    line = '{}={}'.format(
                        match.group(1),
                        converter(match.group(2))
                    )
                except Exception as e:
                    print('line {}: {}'.format(i, e))
            lines.append(line)

    with open(outpath, 'w') as f:
        f.write('\n'.join(lines))


try:
    if len(sys.argv) != 2:
        raise RuntimeError('expected single arguement')
    filepath, ext = path.splitext(sys.argv[1])
    newext, converter = {
        '.attheme': ('.atthex', int_to_hex),
        '.atthex': ('.attheme', hex_to_int)
    }.get(ext, (None, None))
    if not newext:
        raise RuntimeError('what is this file i dont even')
    do_thing(sys.argv[1], filepath + newext, converter)
except RuntimeError as e:
    print('Error:', e)
    print('usage python {} file.[atthex|attheme]'.format(sys.argv[0]))
    exit()