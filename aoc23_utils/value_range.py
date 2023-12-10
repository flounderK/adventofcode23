#!/usr/bin/env python3


class ValueRange:
    def __init__(self, start: int, length: int):
        self.start = start
        self.end = start + length
        self.last = self.end-1
        self.length = length

    def __iter__(self):
        return (self.start, self.last).__iter__()

    def __repr__(self):
        return "ValueRange(%d-%d, length=%d)" % (self.start, self.last, self.length)

    def contains_val(self, val: int) -> bool:
        return self.start <= val and val < self.end

    def _get_min_and_max(self, other: 'ValueRange'):

        if self.start < other.start:
            lower_min, higher_min = self, other
        else:
            lower_min, higher_min = other, self

        if self.end > other.end:
            higher_max, lower_max = self, other
        else:
            higher_max, lower_max = other, self

        return lower_min, higher_min, higher_max, lower_max

    def overlap_check(self, other: 'ValueRange') -> bool:
        if self.start >= other.end or other.start >= self.end:
            return False
        return True

    def intersection(self, other: 'ValueRange') -> 'ValueRange':
        """
        Returns a ValueRange of the intersection between this ValueRange
        and another ValueRange
        """

        if self.overlap_check(other) is False:
            return None

        lower_min, higher_min, higher_max, lower_max = self._get_min_and_max(other)

        # one range fits entirely within the other
        if higher_max == lower_min:
            return ValueRange(lower_max.start, lower_max.length)

        new_range = ValueRange(higher_min.start, lower_max.end-higher_min.start)
        return new_range

    def union(self, other: 'ValueRange') -> 'ValueRange':
        """
        Return a ValueRange that that includes the ranges of two overlapping
        ValueRanges.
        Returns None if ValueRanges
        """
        if self.overlap_check(other) is False:
            return None

        lower_min, higher_min, higher_max, lower_max = self._get_min_and_max(other)
        return ValueRange(lower_min.start, higher_max.end-lower_min.start)

    def __eq__(self, other: 'ValueRange') -> bool:
        if self.start == other.start and self.length == other.length:
            return True
        return False

    def __ne__(self, other: 'ValueRange') -> bool:
        return not (self == other)


def value_range_test():

    # test that equality works
    eq1 = ValueRange(10, 5)
    eq2 = ValueRange(10, 5)
    assert eq1 == eq2

    # test that enclosing regions work with overlap
    ab_overlap = ValueRange(5, 2)
    a = ValueRange(0, 10)
    b = ValueRange(5, 2)
    assert a.intersection(b) == ab_overlap
    assert b.intersection(a) == ab_overlap

    # test that back overlap works
    ac_overlap = ValueRange(7, 3)
    c =  ValueRange(7, 10)
    assert a.intersection(c) == ac_overlap
    assert c.intersection(a) == ac_overlap

    # test that front overlap works
    g = ValueRange(-2, 5)
    ag_overlap = ValueRange(0, 3)
    assert a.intersection(g) == ag_overlap
    assert g.intersection(a) == ag_overlap

    # test that front overlap on shared start works
    ad_overlap = ValueRange(0, 4)
    d = ValueRange(0, 4)
    assert a.intersection(d) == ad_overlap
    assert d.intersection(a) == ad_overlap

    # test that back overlap on shared end works
    af_overlap = ValueRange(7, 3)
    f = ValueRange(7, 3)
    assert a.intersection(f) == af_overlap
    assert f.intersection(a) == af_overlap

    # test non-overlapping works
    h = ValueRange(15, 22)
    assert a.intersection(h) is None
    assert h.intersection(a) is None

    # test non-overlapping but adjacent ranges
    i = ValueRange(10, 5)
    assert a.intersection(i) is None
    assert i.intersection(a) is None

    return True
