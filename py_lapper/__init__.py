"""
py_lapper is an simple datastructure for doing interval queries.

The primary interface for it is via the `find` method. For fast
in-order queries use the `seek` method.
"""

__version__ = "0.9.5"

from .lib import Interval, Cursor, Lapper
