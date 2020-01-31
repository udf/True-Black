# Shows missing/old keys by comparing two themes
# Usage: python keyinfo.py <your theme> <official theme>

import re
import sys
import colorsys
import random

RE_LINE = re.compile(r'^(\w+)=(.+)$')


def get_keys(path):
    keys = set()
    with open(path) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            match = RE_LINE.match(line)
            if not match:
                continue
            keys.add(match.group(1))
    return keys


def get_debug_colour():
    h = random.uniform(0, 1)
    s = random.uniform(0.5, 1)
    v = random.uniform(0.5, 1)
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return ''.join(f'{round(c * 255):02x}' for c in rgb)


try:
    our_keys = get_keys(sys.argv[1])
    official_keys = get_keys(sys.argv[2])

    removed_keys = our_keys - official_keys
    new_keys = official_keys - our_keys

    print(f'Removed keys:')
    for k in removed_keys:
        print(f'{k}=#{get_debug_colour()}')
    print()
    print(f'New keys:')
    for k in new_keys:
        print(f'{k}=#{get_debug_colour()}')
    print()
except RuntimeError as e:
    print('Error:', e)
