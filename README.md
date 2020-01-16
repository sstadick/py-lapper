# py_lapper
[![PyPI version](https://badge.fury.io/py/py-lapper.svg)](https://badge.fury.io/py/py-lapper)
![Coverage](./coverage.svg)


A pure python port of [nim-lapper](https://github.com/brentp/nim-lapper). Please also see the rust lib, [rust-lapper](https://crates.io/crates/rust-lapper)

Stay tuned for a pyO3 wrapper for the rust lib.

## Install

```bash
pip install py_lapper
```

## Usage

```python
from py_lapper import Interval, Lapper, Cursor

intervals = [Interval(0, 5, True), Interval(4, 8, True), Interval(9, 12, True)]
lapper = Lapper(intervals)

found = [iv for iv in lapper.find(4, 7)]
# found = [Interval(0, 5, True), Interval(4, 8, True)]

# Use seek when you will have many queries in sorted order.
cursor = Cursor(0)
found = [iv for iv in lapper.seek(1, 4, cursor)]
# found = [Interval(0, 5, True)]
# cursor = Cursor(2)

found = [iv for iv in lapper.seek(5, 7, cursor)]
# found = [Interval(4, 8, True)]
# cursor = Cursor(3)
```
