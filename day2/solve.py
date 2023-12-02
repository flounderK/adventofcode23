#!/usr/bin/env python3
import re
import argparse
import logging
import functools
import operator


log = logging.getLogger(__file__)
if not log.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s %(message)s")
    log.addHandler(handler)
log.setLevel(logging.DEBUG)


def parse_game_line(line):
    game_header, game_data = line.split(': ')
    game_id_str = game_header.split(' ')[-1]
    game_id = int(game_id_str)
    colors = ["red", "green", "blue"]
    pat = "(?P<NUM>\d+) (?P<COLOR>(?:%s))" % "|".join(colors)
    rexp = re.compile(pat)
    default_round_dict = dict(zip(colors, [0]*len(colors)))
    game_round_strs = game_data.split(';')
    rounds = []
    for round_str in game_round_strs:
        round_dict = default_round_dict.copy()
        for m in re.finditer(rexp, round_str):
            gd = m.groupdict()
            round_dict[gd['COLOR']] = int(gd['NUM'])
        rounds.append(round_dict)

    return game_id, rounds


class Game:
    def __init__(self, game_id, rounds=None):
        self.game_id = game_id
        self.rounds = []
        if rounds:
            self.rounds = rounds

    def exceeds_constraint(self, red=10000, green=10000, blue=10000):
        return (any([r for r in self.rounds
                         if r['red'] > red or
                            r['blue'] > blue or
                            r['green'] > green]))

    def get_smallest_set(self):
        resdict = {"red": 0, "green": 0, "blue": 0}
        for r in self.rounds:
            for k in r.keys():
                val = r[k]
                if val > resdict[k]:
                    resdict[k] = val
        return resdict

    def get_power_of_smallest_set(self):
        small_set = self.get_smallest_set().values()
        return functools.reduce(operator.mul, small_set)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", default="input.txt")
args = parser.parse_args()

with open(args.input, "r") as f:
    data = f.read().splitlines()

games = [Game(*parse_game_line(line)) for line in data]

p1_total = sum([i.game_id for i in games if not i.exceeds_constraint(12, 13, 14)])

print("part 1 %d" % p1_total)

p2_total = sum([g.get_power_of_smallest_set() for g in games])

print("part 2 %d" % p2_total)
