from __future__ import annotations
from typing import TypeVar, Generic, Iterable, Sequence, Iterator

T = TypeVar("T")


class Cursor(object):
    """Cursor is a wrapper for an index to allow for mutation."""

    __slots__ = ["index"]

    def __init__(self, cursor: int) -> None:
        self.index = cursor

    def __repr__(self) -> str:
        """Return the string representation of the cursor."""
        return f"Cursor({self.index})"


class Interval(Generic[T]):
    """Interval represenation that is inclusive start, exclusive stop."""

    __slots__ = ["start", "stop", "val"]

    def __init__(self, start: int, stop: int, val: T):
        self.start = start
        self.stop = stop
        self.val = val

    def overlap(self, other: Interval[T]) -> bool:
        """Return true if `self` overlaps `other`."""
        return self.start < other.stop and self.stop > other.start

    def overlap_pos(self, start: int, stop: int) -> bool:
        """Return true if `self` overlaps the passed in `start` / `stop`."""
        return self.start < stop and self.stop > start

    def __gt__(self, other: Interval[T]) -> bool:
        """Check if `self` is greater than `other`

        Check is based on start first, then stop.
        """
        if self.start > other.start:
            return True
        elif self.start == other.start:
            if self.stop > other.stop:
                return True
        return False

    def __lt__(self, other: Interval[T]) -> bool:
        """Check if `self` is less than `other`

        Check is based on start first, then stop.
        """
        if self.start < other.start:
            return True
        elif self.start == other.start:
            if self.stop < other.stop:
                return True
        return False

    def __eq__(self, other: object) -> bool:
        """Check if two intervals are equal to eachother.
        
        Equality is based on start and stop sites.
        """
        if not isinstance(other, Interval):
            return NotImplemented
        return self.start == other.start and self.stop == other.stop

    def __repr__(self) -> str:
        """String representation of Interval."""
        return f"Interval({self.start}, {self.stop}, {self.val})"


class Lapper(object):
    """Lapper is the primary datastructure for py_lapper.

    Lapper takes in a Sequence of intervals, sorts it, and finds
    the largest interval in the passed in set. The primary methods
    for interacting with Lapper are `find` and `seek`.
    """

    def __init__(self, intervals: Sequence[Interval[T]]) -> None:
        self.intervals = sorted(intervals)
        self.max_len = self._find_max_len(intervals)
        self.cov = None
        self.overlaps_merged = False
        self.cursor = 0

    def __iter__(self) -> Iterable[Interval[T]]:
        """Iterator over intervals in Lapper."""
        return (i for i in self.intervals)

    @staticmethod
    def _find_max_len(intervals: Iterable[Interval[T]]) -> int:
        """Find the max length in the list of intervals."""
        max_len = 0
        max_iv = None
        for iv in intervals:
            if iv.stop - iv.start > max_len:
                max_len = iv.stop - iv.start
                max_iv = iv
        return max_len

    @staticmethod
    def lower_bound(start: int, intervals: Sequence[Interval[T]]) -> int:
        """Find the lowest index that we should start searching from."""
        size = len(intervals)
        low = 0

        while size > 0:
            half = size // 2
            other_half = size - half
            probe = low + half
            other_low = low + other_half
            v = intervals[probe]
            size = half
            low = other_low if v.start < start else low
        return low

    def find(self, start: int, stop: int) -> Iterator[Interval[T]]:
        """Iterate over Intervals that overlap the input `start` and `stop` site."""
        offset = self.lower_bound(start - self.max_len, self.intervals)

        for i in range(offset, len(self.intervals)):
            interval = self.intervals[i]
            if interval.start >= stop:
                break
            elif interval.overlap_pos(start, stop):
                yield interval

    def seek(self, start: int, stop: int, cursor: Cursor) -> Iterator[Interval[T]]:
        """Iterate over Intervals that overlap the input `start` and `stop` site.

        The cursor tracks the position so that the lower_bound does not need to be
        found for each new query. 
        """
        if cursor.index == 0 or (
            cursor.index < len(self.intervals)
            and self.intervals[cursor.index].start > start
        ):
            cursor.index = self.lower_bound((start - self.max_len), self.intervals)

        while (
            cursor.index + 1 < len(self.intervals)
            and self.intervals[cursor.index + 1].start < start - self.max_len
        ):
            cursor.index += 1

        for i in range(cursor.index, len(self.intervals)):
            interval = self.intervals[i]
            if interval.start >= stop:
                break
            elif interval.overlap_pos(start, stop):
                yield interval
