import pytest
from py_lapper import __version__
from py_lapper import Lapper, Interval, Cursor


def setup_nonoverlapping():
    data = [Interval(x, x + 10, 0) for x in range(0, 100, 20)]
    lapper = Lapper(data)
    return lapper


def setup_overlapping():
    data = [Interval(x, x + 15, 0) for x in range(0, 100, 10)]
    lapper = Lapper(data)
    return lapper


def setup_bad_lapper():
    data = [
        Interval(start=70, stop=120, val=0),  # max_len = 50
        Interval(start=10, stop=15, val=0),
        Interval(start=10, stop=15, val=0),  # exact overlap
        Interval(start=12, stop=15, val=0),  # inner overlap
        Interval(start=14, stop=16, val=0),  # overlap end
        Interval(start=40, stop=45, val=0),
        Interval(start=50, stop=55, val=0),
        Interval(start=60, stop=65, val=0),
        Interval(start=68, stop=71, val=0),  # overlap start
        Interval(start=70, stop=75, val=0),
    ]
    return Lapper(data)


def setup_single():
    return Lapper([Interval(10, 35, 0)])


def test_version():
    assert __version__ == "0.9.5"


def test_lower_bound():
    """Test that the rightmost index starting from the left is found for hte start given"""
    lapper = setup_bad_lapper()
    rightmost = lapper.lower_bound(38, lapper.intervals)
    assert rightmost == 4


# def test_benchmark_lower_bound(benchmark):
#     """Test that the rightmost index starting from the left is found for hte start given"""

#     def bench_lower():
#         found = lapper.lower_bound(499_999, intervals)
#         return found

#     lapper = setup_bad_lapper()
#     intervals = [Interval(x, x + 10, 0) for x in range(0, 10000000, 20)]
#     rightmost = benchmark(bench_lower)
#     assert rightmost == 25000


def test_query_stop_interval_start():
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    with pytest.raises(StopIteration):
        next(lapper.find(15, 20))
    with pytest.raises(StopIteration):
        next(lapper.seek(15, 20, cursor))


def test_query_start_interval_stop():
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    with pytest.raises(StopIteration):
        next(lapper.find(30, 35))
    with pytest.raises(StopIteration):
        next(lapper.seek(30, 35, cursor))


def test_query_overlaps_interval_start():
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    expected = Interval(20, 30, 0)

    assert expected == next(lapper.find(15, 25))
    assert expected == next(lapper.seek(15, 25, cursor))
    assert list(lapper.find(15, 25)) == list(lapper.seek(15, 25, Cursor(0)))


def test_query_overlaps_interval_stop():
    """Test that a query that overlaps the stop of an interval returns that interval"""
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    expected = Interval(20, 30, 0)

    assert expected == next(lapper.find(25, 35))
    assert expected == next(lapper.seek(25, 35, cursor))
    assert list(lapper.find(25, 35)) == list(lapper.seek(25, 35, Cursor(0)))


def test_interval_envelops_query():
    """Test that a query that is enveloped by interval returns interval"""
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    expected = Interval(20, 30, 0)

    assert expected == next(lapper.find(22, 27))
    assert expected == next(lapper.seek(22, 27, cursor))
    assert list(lapper.find(22, 27)) == list(lapper.seek(22, 27, Cursor(0)))


def test_query_envelops_interval():
    """Test that a query that envolops an interval returns that interval"""
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    expected = Interval(20, 30, 0)

    assert expected == next(lapper.find(15, 35))
    assert expected == next(lapper.seek(15, 35, cursor))
    assert list(lapper.find(15, 35)) == list(lapper.seek(15, 35, Cursor(0)))


def test_overlapping_intervals():
    """Test interval overlaps are working properly"""
    lapper = setup_overlapping()
    cursor = Cursor(0)
    e1 = Interval(0, 15, 0)
    e2 = Interval(10, 25, 0)
    assert [e1, e2] == list(lapper.find(8, 20))
    assert [e1, e2] == list(lapper.seek(8, 20, cursor))
    assert list(lapper.find(8, 20)) == list(lapper.seek(8, 20, Cursor(0)))


def test_seek_over_len():
    """Test that it's not possible to induce index out of bounds by pushing the cursor past the end of the lapper."""
    lapper = setup_nonoverlapping()
    single = setup_single()
    cursor = Cursor(0)

    for interval in lapper.intervals:
        for o_interval in single.seek(interval.start, interval.stop, cursor):
            print(o_interval)


def test_find_over_behind_first_match():
    """Test that if lower_bound puts us before the first match, we still return a match"""
    lapper = setup_bad_lapper()
    e1 = Interval(50, 55, 0)
    found = next(lapper.find(50, 55))
    assert found == e1
    assert list(lapper.find(50, 55)) == list(lapper.seek(50, 55, Cursor(0)))


def test_find_over_nonoverlapping():
    """Test that seeking for all intervals over self == len(self)"""
    lapper = setup_nonoverlapping()
    total = 0
    for iv in lapper:
        total += sum(1 for _ in lapper.find(iv.start, iv.stop))
    assert total == len(lapper.intervals)


def test_seek_over_nonoverlapping():
    """Test that seeking for all intervals over self == len(self)"""
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    total = 0
    for iv in lapper:
        for fiv in lapper.seek(iv.start, iv.stop, cursor):
            total += 1
    assert total == len(lapper.intervals)


def test_seek_over_overlapping():
    """Test that seeking for all intervals over self == len(self)"""
    lapper = setup_overlapping()
    cursor = Cursor(0)
    total = 0
    for iv in lapper:
        for fiv in lapper.seek(iv.start, iv.stop, cursor):
            total += 1
    assert total == 28


def test_find_over_overlapping():
    """Test that seeking for all intervals over self == len(self)"""
    lapper = setup_overlapping()
    total = 0
    for iv in lapper:
        for fiv in lapper.find(iv.start, iv.stop):
            total += 1
    assert total == 28


def test_seek_over_short_stop():
    """Test that seek is not stopping early"""
    lapper = Lapper([Interval(0, 1, 0), Interval(0, 1, 0), Interval(1, 2, 0),])
    cursor = Cursor(0)

    seek_total = 0
    for iv in lapper:
        for fiv in lapper.seek(iv.start, iv.stop, cursor):
            seek_total += 1
    find_total = 0
    for iv in lapper:
        for fiv in lapper.find(iv.start, iv.stop):
            find_total += 1
    assert seek_total == 5
    assert find_total == 5


def test_bad_skips():
    """When there is a very long interval that spans many little intervals, test that the little intevals still get returne properly"""
    data = [
        Interval(25264912, 25264986, 0),
        Interval(27273024, 27273065, 0),
        Interval(27440273, 27440318, 0),
        Interval(27488033, 27488125, 0),
        Interval(27938410, 27938470, 0),
        Interval(27959118, 27959171, 0),
        Interval(28866309, 33141404, 0),
    ]
    lapper = Lapper(data)
    found = list(lapper.find(28974798, 33141355))
    assert found == [Interval(28866309, 33141404, 0)]
    assert list(lapper.find(28974798, 33141355)) == list(
        lapper.seek(28974798, 33141355, Cursor(0))
    )

