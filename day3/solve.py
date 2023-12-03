#!/usr/bin/env python3
import re
import aoc23_utils
from aoc23_utils import log, cli
from aoc23_utils import GridPoint, GridPointRange
from collections import defaultdict
import operator
import functools




class SchematicNumber:
    def __init__(self, value, grid_point_range):
        self.value = value
        self.gpr = grid_point_range

    def __repr__(self):
        return "SchematicNumber(%d, (%d-%d, %d-%d))" % (self.value,
                                                        self.gpr.start_x,
                                                        self.gpr.end_x,
                                                        self.gpr.start_y,
                                                        self.gpr.end_y)

class SymPoint:
    def __init__(self, sym, grid_point):
        self.gp = grid_point
        self.sym = sym


def parse_from_grid_lines(grid_lines):
    rexp = re.compile("((?P<NUM>\d+)|(?P<SYM>[^0-9.]))")
    schematic_numbers = []
    symb_points = []
    for y, line in enumerate(grid_lines):
        for m in re.finditer(rexp, line):
            gd = m.groupdict()
            if gd.get("NUM"):
                start_x, end_x = m.span()
                value = int(m.groups()[0])
                # end value is meant for indexing, so it is one
                # past the last character's index
                gpr = GridPointRange((start_x, end_x-1), y)
                num = SchematicNumber(value, gpr)
                schematic_numbers.append(num)
            elif gd.get("SYM"):
                gp = GridPoint(m.start(), y)
                sym_point = SymPoint(m.groups()[0], gp)
                symb_points.append(sym_point)

    return symb_points, schematic_numbers


data_raw = cli()
data = data_raw.split("\n")
symb_points, schematic_numbers = parse_from_grid_lines(data)

p1_total = 0
are_adjacent = set()
adj_dict = defaultdict(set)
for num in schematic_numbers:
    for sym_point in symb_points:
        if num.gpr.is_adjacent(sym_point.gp, diagonal=True):
            are_adjacent.add(num)
            adj_dict[sym_point].add(num)

for num in are_adjacent:
    p1_total += num.value
print(p1_total)

gear_ratios = []
for sym_point, nums in adj_dict.items():
    if sym_point.sym != '*':
        continue
    if len(nums) != 2:
        continue
    gear_ratio = functools.reduce(operator.mul, [i.value for i in nums])
    gear_ratios.append(gear_ratio)

gear_ratio_sum = sum(gear_ratios)
print("part 2 %d" % gear_ratio_sum)
