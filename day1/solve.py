#!/usr/bin/env python3
import re
import argparse
import logging


log = logging.getLogger(__file__)
if not log.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s %(message)s")
    log.addHandler(handler)
log.setLevel(logging.DEBUG)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", default="input.txt")
args = parser.parse_args()

with open(args.input, "r") as f:
    data = f.read().splitlines()

rexp = re.compile("(\d)")

p1_total = 0
for line in data:
    match_digits = re.findall(rexp, line)
    if len(match_digits) == 0:
        continue
    value = int(match_digits[0] + match_digits[-1])
    p1_total += value

print("part 1 %d" % p1_total)


digit_names = "one, two, three, four, five, six, seven, eight, nine".split(', ')

digit_name_map = dict(zip(digit_names, [str(i) for i in range(1, 10)]))

digit_name_pat = '|'.join(list(digit_name_map.keys()))
# lookahead assertion to allow overlapping matches
full_pattern = "(?=(%s))" % "|".join(["\d", digit_name_pat])

print("rexp '%s'" % full_pattern)

rexp2 = re.compile(full_pattern)

p2_total = 0
for line in data:
    log.debug("line: '%s'" % line)
    matches = re.findall(rexp2, line)
    if len(matches) == 0:
        log.warning("skipping line '%s'" % line)
        continue
    first_match = matches[0]
    last_match = matches[-1]
    log.debug("first_match '%s'", first_match)
    log.debug("last_match '%s'", last_match)
    first = digit_name_map.get(first_match, first_match)
    last = digit_name_map.get(last_match, last_match)
    value = int(first + last)
    log.debug("made value '%d'", value)
    p2_total += value
    log.debug("")

print("part 2 %d" % p2_total)
