#!/usr/bin/env python3
import re
from aoc23_utils import cli, log
import logging
from collections import defaultdict
import enum


class CardHandCategory(enum.IntEnum):
    NONE_HAND = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_KIND = 4
    FULL_HOUSE = 5
    FOUR_KIND = 6
    FIVE_KIND = 7


JOKER_ENABLED = False
CARD_PRIORITY_MAP = {str(i): i for i in range(2, 10)}
face_cards = ["T", "J", "Q", "K", "A"]
fcm = dict(zip(face_cards, range(10, 10+len(face_cards)+1)))
CARD_PRIORITY_MAP.update(fcm)

# value count lists
FIVE_KIND_LIST = [5]
FOUR_KIND_LIST = [1, 4]
FULL_HOUSE_LIST = [2, 3]
THREE_KIND_LIST = [1, 1, 3]
TWO_PAIR_LIST = [1, 2, 2]
ONE_PAIR_LIST = [1, 1, 1, 2]
HIGH_CARD_LIST = [1, 1, 1, 1, 1]

NORMAL_VALUE_COUNT_LOOKUP = [
    (FIVE_KIND_LIST, CardHandCategory.FIVE_KIND),
    (FOUR_KIND_LIST, CardHandCategory.FOUR_KIND),
    (FULL_HOUSE_LIST, CardHandCategory.FULL_HOUSE),
    (THREE_KIND_LIST, CardHandCategory.THREE_KIND),
    (TWO_PAIR_LIST, CardHandCategory.TWO_PAIR),
    (ONE_PAIR_LIST, CardHandCategory.ONE_PAIR),
    (HIGH_CARD_LIST, CardHandCategory.HIGH_CARD)
]

VALUE_COUNT_LOOKUP = NORMAL_VALUE_COUNT_LOOKUP


def get_high_card_priority(cardstr):
    global CARD_PRIORITY_MAP
    highest = 0
    for c in cardstr:
        val = CARD_PRIORITY_MAP.get(c, 0)
        if val > highest:
            highest = val
    return highest


def joker_upgrade(cardstr, category):
    joker_count = cardstr.count("J")
    if joker_count == 0:
        return category
    if category == CardHandCategory.HIGH_CARD:
        return CardHandCategory.ONE_PAIR
    if category == CardHandCategory.ONE_PAIR:
        # could upgrade to two pair if there is 1 J,
        # but always prefer three kind with 1 J or 2 J
        # because it is a better hand
        return CardHandCategory.THREE_KIND

    if category == CardHandCategory.TWO_PAIR:
        if joker_count == 1:
            return CardHandCategory.FULL_HOUSE
        elif joker_count == 2:
            return CardHandCategory.FOUR_KIND
    if category == CardHandCategory.THREE_KIND:
        # reachable either with 3 J or 1 J,
        # could also upgrade to FULL_HOUSE, with 1 J,
        # but FOUR_KIND is reachable in both cases
        # and is a better hand
        return CardHandCategory.FOUR_KIND
    if category in [CardHandCategory.FULL_HOUSE,
                    CardHandCategory.FOUR_KIND,
                    CardHandCategory.FIVE_KIND,
                   ]:
        # reachable with 2 J or 3 J for FULL_HOUSE
        # reachable with 4 J or 1 J for FOUR_KIND
        # reachable with 5 J for FIVE_KIND
        return CardHandCategory.FIVE_KIND



def categorize_card_str(cardstr):
    global VALUE_COUNT_LOOKUP
    global JOKER_ENABLED
    log.debug("cardstr %s" % cardstr)
    count_dict_dd = defaultdict(lambda: 0)

    for c in cardstr:
        count_dict_dd[c] += 1
    # convert the count dict back to a normal dict
    count_dict = dict(count_dict_dd)
    card_count_list = list(count_dict.values())
    card_count_list.sort()
    log.debug("card count %s" % str(card_count_list))
    # look up the counts of all cards, as counts will remain
    # the same regardless of which cards are present
    category = CardHandCategory.NONE_HAND
    for vc_list, enum_val in VALUE_COUNT_LOOKUP:
        # log.debug("vc_list = %s" % str(vc_list))
        if card_count_list == vc_list:
            log.debug("chose %s" % enum_val.name)
            category = enum_val
            break
    if category == CardHandCategory.NONE_HAND:
        raise Exception("Unhandled hand %s" % cardstr)
    if JOKER_ENABLED and "J" in cardstr:
        joker_count = count_dict.get("J", 0)
        log.debug("joker count %d" % joker_count)
        category = joker_upgrade(cardstr, category)
        log.debug("adjusted to %s" % category.name)

    return category


def card_str_cmp(a_cardstr, b_cardstr):
    global CARD_PRIORITY_MAP
    for a, b in zip(a_cardstr, b_cardstr):
        a_val = CARD_PRIORITY_MAP.get(a, 0)
        b_val = CARD_PRIORITY_MAP.get(b, 0)
        if a_val == b_val:
            continue
        if a_val > b_val:
            return 1
        if b_val > a_val:
            return -1
    return 0


class CardHand:
    def __init__(self, cardstr):
        self.cardstr = cardstr
        self.high_card_priority = 0
        self.category = categorize_card_str(cardstr)
        if self.category == CardHandCategory.HIGH_CARD:
            self.high_card_priority = get_high_card_priority(cardstr)

    def __repr__(self):
        return "CardHand(%s, %s)" % (self.cardstr, self.category.name)

    def __gt__(self, other: 'CardHand') -> bool:
        if self.category > other.category:
            return True
        if self.category < other.category:
            return False
        if card_str_cmp(self.cardstr, other.cardstr) == 1:
            return True
        return False

    def __lt__(self, other: 'CardHand') -> bool:
        if self.category < other.category:
            return True
        if self.category > other.category:
            return False
        if card_str_cmp(self.cardstr, other.cardstr) == -1:
            return True
        return False

    def __eq__(self, other: 'CardHand') -> bool:
        if self.category != other.category:
            return False
        if self.cardstr != other.cardstr:
            return False
        return True

    def __ne__(self, other: 'CardHand') -> bool:
        return not (self == other)


class CamelCardHand:
    def __init__(self, cardstr, bid):
        self.cardstr = cardstr
        self.card_hand = CardHand(cardstr)
        self.bid = bid
    def __repr__(self):
        return "CamelCardHand(%s, %s, bid=%d)" % \
                (self.cardstr, self.card_hand.category.name,
                 self.bid)


data = cli()
card_hands = []
for line in data.splitlines():
    cardstr, bidstr = line.split(" ")
    bid = int(bidstr)
    hand = CamelCardHand(cardstr, bid)
    card_hands.append(hand)


card_hands.sort(key=lambda a: a.card_hand)
p1_total = sum([cch.bid*(i+1) for i,cch in enumerate(card_hands)])
print("part 1 %d" % p1_total)

CARD_PRIORITY_MAP.pop("J")
CARD_PRIORITY_MAP['J'] = 1
JOKER_ENABLED = True
p2_card_hands = []
for line in data.splitlines():
    cardstr, bidstr = line.split(" ")
    bid = int(bidstr)
    hand = CamelCardHand(cardstr, bid)
    p2_card_hands.append(hand)

p2_card_hands.sort(key=lambda a: a.card_hand)
p2_total = sum([cch.bid*(i+1) for i,cch in enumerate(p2_card_hands)])
print("part 2 %d" % p2_total)


