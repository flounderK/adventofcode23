#!/usr/bin/env python3
import re
from aoc23_utils import log, cli
from collections import defaultdict


data = cli()

data_lines = data.splitlines()
parsed = [i.split(': ')[-1].split(' | ') for i in data_lines]

win_list = []
copy_map = defaultdict(lambda: 1)
p1_total = 0
for i, [winning_card, my_card] in enumerate(parsed):
    pattern = r'\b(%s)\b' % \
              '|'.join([i.groups()[0] for i in re.finditer("(\d+)", winning_card)])
    log.debug("pattern '%s'", pattern)
    win_count = 0
    copy_map[i+1] += 0
    for m in re.finditer(pattern, my_card):
        log.debug("%s" % str(m.groups()[0]))
        win_count += 1
        copy_map[i+1+win_count] += 1
    win_list.append(win_count)
    # log.debug("card %d: %d" % (i+1, win_count))
    if win_count > 0:
        p1_total += 2**(win_count-1)

print("part 1: %d" % p1_total)


