class Cursor(object):
    __slots__ = ["index"]

    def __init__(self, cursor):
        self.index = cursor

    def inc(self):
        self.index += 1

    def set(self, val):
        self.index = val

    def val(self):
        return self.index

    def __repr__(self):
        return f"Cursor({self.index})"


class Interval(object):
    __slots__ = ["start", "stop", "val"]

    def __init__(self, start, stop, val):
        self.start = start
        self.stop = stop
        self.val = val

    def overlap(self, other):
        return self.start < other.stop and self.stop > other.start

    def overlap_pos(self, start, stop):
        return self.start < stop and self.stop > start

    def __gt__(self, other):
        if self.start > other.start:
            return True
        elif self.start == other.start:
            if self.stop > other.stop:
                return True
        return False

    def __lt__(self, other):
        if self.start < other.start:
            return True
        elif self.start == other.start:
            if self.stop < other.stop:
                return True
        return False

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop

    def __repr__(self):
        return f"Interval({self.start}, {self.stop}, {self.val})"


class Lapper(object):
    def __init__(self, intervals):
        self.intervals = sorted(intervals)
        self.max_len = self._find_max_len(intervals)
        self.cov = None
        self.overlaps_merged = False
        self.cursor = 0

    @staticmethod
    def _find_max_len(intervals):
        """Find the max length in the list of intervals.
        """
        max_len = 0
        max_iv = None
        for iv in intervals:
            if iv.stop - iv.start > max_len:
                max_len = iv.stop - iv.start
                max_iv = iv
        return max_len

    @staticmethod
    def lower_bound(start, intervals):
        """Find the lowest index that we should start searching from.
        """
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

    def find(self, start, stop):
        offset = self.lower_bound(start - self.max_len, self.intervals)

        while offset < len(self.intervals):
            interval = self.intervals[offset]
            offset += 1
            if interval.overlap_pos(start, stop):
                yield interval
            elif interval.start >= stop:
                break

    def seek(self, start, stop, cursor):
        """Find overlaps when querying in a known sequential order.
        """
        if cursor.val() == 0 or (
            cursor.val() < len(self.intervals)
            and self.intervals[cursor.val()].start > start
        ):
            cursor.set(self.lower_bound((start - self.max_len), self.intervals))

        while (
            cursor.val() + 1 < len(self.intervals)
            and self.intervals[cursor.val() + 1].start < start - self.max_len
        ):
            cursor.inc()

        while cursor.val() < len(self.intervals):
            interval = self.intervals[cursor.val()]
            cursor.inc()
            if interval.overlap_pos(start, stop):
                yield interval
            elif interval.start >= stop:
                break
