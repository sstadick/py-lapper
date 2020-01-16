import pytest
from py_lapper import __version__
from py_lapper.lib import Lapper, Interval, Cursor


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


# TESTS


def test_version():
    assert __version__ == "0.1.0"


def test_query_stop_interval_start():
    lapper = setup_nonoverlapping()
    cursor = Cursor(0)
    with pytest.raises(StopIteration):
        next(lapper.find(15, 20))
    with pytest.raises(StopIteration):
        next(lapper.seek(15, 20, cursor))
    # assert len(list(lapper.find(15, 20))) == lapper.count(15, 20)

    # // Test that a query stop that hits an interval start returns no interval
    # #[test]
    # fn test_query_stop_interval_start() {
    # let lapper = setup_nonoverlapping();
    # let mut cursor = 0;
    # assert_eq!(None, lapper.find(15, 20).next());
    # assert_eq!(None, lapper.seek(15, 20, &mut cursor).next());
    # assert_eq!(lapper.find(15, 20).count(), lapper.count(15, 20));
    # }

    # // Test that a query start that hits an interval end returns no interval
    # #[test]
    # fn test_query_start_interval_stop() {
    # let lapper = setup_nonoverlapping();
    # let mut cursor = 0;
    # assert_eq!(None, lapper.find(30, 35).next());
    # assert_eq!(None, lapper.seek(30, 35, &mut cursor).next());
    # assert_eq!(lapper.find(30, 35).count(), lapper.count(30, 35));
    # }

    # // Test that a query that overlaps the start of an interval returns that interval
    # #[test]
    # fn test_query_overlaps_interval_start() {
    # let lapper = setup_nonoverlapping();
    # let mut cursor = 0;
    # let expected = Iv {
    # start: 20,
    # stop: 30,
    # val: 0,
    # };
    # assert_eq!(Some(&expected), lapper.find(15, 25).next());
    # assert_eq!(Some(&expected), lapper.seek(15, 25, &mut cursor).next());
    # assert_eq!(lapper.find(15, 25).count(), lapper.count(15, 25));
    # }

    # // Test that a query that overlaps the stop of an interval returns that interval
    # #[test]
    # fn test_query_overlaps_interval_stop() {
    # let lapper = setup_nonoverlapping();
    # let mut cursor = 0;
    # let expected = Iv {
    # start: 20,
    # stop: 30,
    # val: 0,
    # };
    # assert_eq!(Some(&expected), lapper.find(25, 35).next());
    # assert_eq!(Some(&expected), lapper.seek(25, 35, &mut cursor).next());
    # assert_eq!(lapper.find(25, 35).count(), lapper.count(25, 35));
    # }

    # // Test that a query that is enveloped by interval returns interval
    # #[test]
    # fn test_interval_envelops_query() {
    # let lapper = setup_nonoverlapping();
    # let mut cursor = 0;
    # let expected = Iv {
    # start: 20,
    # stop: 30,
    # val: 0,
    # };
    # assert_eq!(Some(&expected), lapper.find(22, 27).next());
    # assert_eq!(Some(&expected), lapper.seek(22, 27, &mut cursor).next());
    # assert_eq!(lapper.find(22, 27).count(), lapper.count(22, 27));
    # }

    # // Test that a query that envolops an interval returns that interval
    # #[test]
    # fn test_query_envolops_interval() {
    # let lapper = setup_nonoverlapping();
    # let mut cursor = 0;
    # let expected = Iv {
    # start: 20,
    # stop: 30,
    # val: 0,
    # };
    # assert_eq!(Some(&expected), lapper.find(15, 35).next());
    # assert_eq!(Some(&expected), lapper.seek(15, 35, &mut cursor).next());
    # assert_eq!(lapper.find(15, 35).count(), lapper.count(15, 35));
    # }

    # #[test]
    # fn test_overlapping_intervals() {
    # let lapper = setup_overlapping();
    # let mut cursor = 0;
    # let e1 = Iv {
    # start: 0,
    # stop: 15,
    # val: 0,
    # };
    # let e2 = Iv {
    # start: 10,
    # stop: 25,
    # val: 0,
    # };
    # assert_eq!(vec![&e1, &e2], lapper.find(8, 20).collect::<Vec<&Iv>>());
    # assert_eq!(
    # vec![&e1, &e2],
    # lapper.seek(8, 20, &mut cursor).collect::<Vec<&Iv>>()
    # );
    # assert_eq!(lapper.count(8, 20), 2);
    # }
