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


def cli(args=None, namespace=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="input.txt")
    args = parser.parse_args(args=args, namespace=namespace)

    with open(args.input, "r") as f:
        data = f.read()
    return data

from .grid import GridPoint, GridPointRange
from .value_range import ValueRange
from .binary_tree import BinaryTreeNode, BinaryTreeDir
