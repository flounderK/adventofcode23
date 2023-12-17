#!/usr/bin/env python3
import re
from aoc23_utils import cli, log, BinaryTreeDir, BinaryTreeNode
import logging
import enum
from collections import deque, defaultdict


class NamedBinaryTreeNode(BinaryTreeNode):
    def __init__(self, name, left=None, right=None):
        self.name = name
        super().__init__(left, right)

    def __repr__(self):
        return "NBTN(%s)" % self.name


def binary_tree_follow_instr_to_node(start_node, end_node, instructions):
    instructions = instructions.copy()
    count = 0
    node = start_node
    while node != end_node:
        node = node.get_child(instructions[0])
        count += 1
        instructions.rotate(-1)
    return count


data = cli()

instructions, node_def_lines = data.split("\n\n")

rexp = re.compile("(\S+) = \(([^,]+), (\S+)\)")

node_def_groups = [m.groups() for m in re.finditer(rexp, node_def_lines)]
node_def_lookup_table = {a: (b, c) for a, b, c in node_def_groups}
node_lookup = {a: NamedBinaryTreeNode(a) for a in node_def_lookup_table.keys()}

for name, [left, right] in node_def_lookup_table.items():
    node = node_lookup[name]
    node.left = node_lookup[left]
    node.right = node_lookup[right]


instruction_list = deque()
for c in instructions:
    if c == "R":
        instruction_list.append(BinaryTreeDir.RIGHT)
    if c == "L":
        instruction_list.append(BinaryTreeDir.LEFT)


start_node = node_lookup['AAA']
end_node = node_lookup['ZZZ']

p1_count = binary_tree_follow_instr_to_node(start_node, end_node, instruction_list)
print("part 1 %d" % p1_count)
initial_instruction_list = instruction_list.copy()

start_nodes = [i for i in node_lookup.values() if i.name.endswith("A")]

loop_counts = {}
visit_lists = defaultdict(list)

for node in start_nodes:
    instruction_list = initial_instruction_list
    initial_node = node
    count = 0
    found_loop = False
    log.debug("starting node %s", node.name)
    while not found_loop:
        node = node.get_child(instruction_list[0])
        visit_lists[initial_node.name].append(node)
        count += 1
        instruction_list.rotate(-1)
        if node.name.endswith("Z") and count != 0:
            log.debug("found loop for %s to %s at count %d", initial_node.name, node.name, count)
            found_loop = True
    loop_counts[initial_node.name] = count




# really inefficient
# p2_count = 0
# node = start_node
# current_nodes = start_nodes.copy()
# while not all([n.name.endswith("Z") for n in current_nodes]):
#     current_nodes = [n.get_child(instruction_list[0]) for n in current_nodes]
#     p2_count += 1
#     instruction_list.rotate(-1)
#
# print("part 2 %d" % p2_count)
