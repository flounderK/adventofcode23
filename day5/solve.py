#!/usr/bin/env python3
import re
from aoc23_utils import cli, log, ValueRange
from collections import namedtuple
import logging


class RangeRule:
    def __init__(self, dest_start, src_start, length):
        self.dest = ValueRange(dest_start, length)
        self.src = ValueRange(src_start, length)
        self.length = length

    @property
    def dest_start(self):
        return self.dest.start

    @property
    def dest_end(self):
        return self.dest.end

    @property
    def dest_last(self):
        return self.dest.last

    @property
    def src_start(self):
        return self.src.start

    @property
    def src_end(self):
        return self.src.end

    @property
    def src_last(self):
        return self.src.last

    def __repr__(self):
        return "RangeRule(dst=%d-%d, src=%d-%d, length=%d)" % (
            self.dest_start, self.dest_last,
            self.src_start, self.src_last,
            self.length)


class MapRules:
    def __init__(self, name):
        name_rexp = re.compile("(\S+)-to-(\S+)")
        self.name = name
        self.rules = []
        self._from = ''
        self._to = ''
        m = re.search(name_rexp, name)
        if m is not None:
            self._from, self._to = m.groups()
    def __repr__(self):
        return "MapRules(%s, %d rules)" % (self.name, len(self.rules))

    def lookup_dest(self, src):
        for rule in self.rules:
            if rule.src.contains_val(src):
                src_off = src - rule.src_start
                return rule.dest_start + src_off
        return src


def batch(it, sz):
    for i in range(0, len(it), sz):
        yield it[i:i+sz]


data_raw = cli()
sections = data_raw.split("\n\n")
num_rexp = re.compile("(\d+)")
seeds = [int(i) for i in re.findall(num_rexp, sections[0])]

name_rexp = re.compile('(\S+) map:')

map_rules_list = []

for section in sections[1:]:
    split_section = section.splitlines()
    rule_lines = split_section[1:]
    name_line = split_section[0]
    name = re.search(name_rexp, name_line).groups()[0]
    map_rules = MapRules(name)
    for line in rule_lines:
        rr = RangeRule(*[int(i) for i in re.findall(num_rexp, line)])
        map_rules.rules.append(rr)
    map_rules_list.append(map_rules)


locations = []
for seed in seeds:
    curr_val = seed
    debug_str = "seed %d" % curr_val
    for map_rules in map_rules_list:
        curr_val = map_rules.lookup_dest(curr_val)
        debug_str += ", %s %d" % (map_rules._to, curr_val)
    log.debug(debug_str)
    locations.append(curr_val)

print("part 1 %d" % min(locations))

# RuleIntersection = namedtuple("RuleIntersection", ["intersect", "rule"])
#
# p2_locations = []
# seed_ranges = []
# for seed_start, seed_len in batch(seeds, 2):
#     seed_range = ValueRange(seed_start, seed_len)
#     seed_ranges.append(seed_range)
#
# reverse_map_rules_list = map_rules_list[::-1]
# lowest_dest_range_rule = None
# # get the rule that will output the lowest dest range for this mapping
# for rule in reverse_map_rules_list[0].rules:
#     if lowest_dest_range_rule is None or rule.dest_start < lowest_dest_range_rule.dest.start:
#         lowest_dest_range_rule = rule
#
# current_target_src = lowest_dest_range_rule.src
# # find the rule that maps
# for map_rules in reverse_map_rules_list[1:]:
#     # get all of the intersections of this MapRules.rules.dest with the src
#     # for the rule that is currently being targeted
#     rule_intersections = []
#     # get all of the rules that can intersect with the target ValueRange
#     for rule in map_rules.rules:
#         intersect = rule.dest.intersection(current_target_src)
#         if intersect is None:
#             continue
#         rule_intersections.append(RuleIntersection(intersect, rule))
#
#     # sort the intersections (which must be valid for the current
#     # target ValueRange already) by where the intersection starts
#     rule_intersections.sort(key=lambda a: a.intersect.start)
#     for

