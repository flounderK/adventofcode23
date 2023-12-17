#!/usr/bin/env python3
import re
from aoc23_utils import cli, log
import logging
from collections import namedtuple
import operator
import functools


RaceData = namedtuple("RaceData", ["time", "record_distance"])


def calc_dist(hold_time, total_time):
    return hold_time*(total_time-hold_time)


data = cli()

rexp = re.compile("(\d+)")
parsed_values = [[int(k) for k in re.findall(rexp, i)] for i in data.splitlines()]

race_datas = [RaceData(*i) for i in zip(*parsed_values)]


num_ways_to_win = []
for rd in race_datas:
    log.debug("Race time %d, distance record %d", rd.time, rd.record_distance)
    curr_ways_to_win = 0
    for hold_time in range(rd.time+1):
        traveled = calc_dist(hold_time, rd.time)
        log.debug("Hold the button for %d milliseconds, the boat will have gone %d millimeters", hold_time, traveled)
        if traveled > rd.record_distance:
            curr_ways_to_win += 1
    num_ways_to_win.append(curr_ways_to_win)
    log.debug("Ways to win %d", curr_ways_to_win)
    log.debug("")

p1_total = functools.reduce(operator.mul, num_ways_to_win)

print("part 1 %d" % p1_total)


def calc_ways_to_win(race_data):
    """
    distance can be calculated as dist = hold_time*(total_time-hold_time)
    which forms a parabola with a peak distance at total_time//2.
    Because it is a parabola, the distances travelled mirror eachother
    around the peak distance, so calculating the number of distances
    that are reachable with whole-number hold times
    between the record distance and peak distance on one side of
    the parabola is all that really needs to be done to find the total
    number of ways to win
    """
    rd = race_data
    log.debug("Race time %d, distance record %d", rd.time, rd.record_distance)
    peak_hold_time = rd.time//2
    peak_dist = calc_dist(peak_hold_time, rd.time)
    log.debug("peak hold time %d, peak dist %d", peak_hold_time, peak_dist)
    hold_time = peak_hold_time
    dist = peak_dist
    ways_to_win = 0
    while dist > rd.record_distance:
        ways_to_win += 1
        hold_time -= 1
        dist = calc_dist(hold_time, rd.time)

    ways_to_win = ways_to_win*2
    if rd.time % 2 == 0:
        ways_to_win -= 1
    return ways_to_win


p2_parsed_values = [int(''.join([k for k in re.findall(rexp, i)])) for i in data.splitlines()]
p2_rd = RaceData(*p2_parsed_values)
rd = p2_rd
p2_ways_to_win = calc_ways_to_win(rd)
print("part 2 %d" % p2_ways_to_win)
