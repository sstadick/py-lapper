# py_lapper

A pure python port of nim-lapper. Please also the rust lib, rust-lapper

Stay tuned for scailist as well

## Install

```bash
# Not yet on pypi
# pip install py_lapper
```

## Usage

```python
from py_lapper import Interval, Lapper, Cursor

intervals = [Interval(0, 5, True), Interval(4, 8, True), Interval(9, 12,
True)]

lapper = Lapper(intervals)

for iv in lapper.find(4, 7):
	print(iv)

# Use seek when you will have many queries in sorted order. 
cursor = Cursor(0)
for iv in lapper.seek(1, 4, cursor):
	print(iv)
print(cursor)

for iv in lapper.seek(5, 7, cursor):
	print(iv)
print(curosr)
```
