Performance
===========

Great efforts were put to make PyFDE honor the *fast* in its name.

The table below lists the results obtained by *tests/perf.py* compared to
other differential evolution implementation, namely Solver-DE (C++),
lua-de (Lua), and a pure Python 3 version.

All versions were implemented by me, so they all did the same work.

+----------------+-----------------+------------+
| Implementation | Total time (ms) | Normalized |
+================+=================+============+
| solver-de      | 42              | 1.00       |
+----------------+-----------------+------------+
| **PyFDE**      | **49**          | **1.17**   |
+----------------+-----------------+------------+
| lua-de (LuaJIT)| 78              | 1.85       |
+----------------+-----------------+------------+
| lua-de (Lua5.1)| 534             | 12.71      |
+----------------+-----------------+------------+
| Pure Python    | 3300            | 78.57      |
+----------------+-----------------+------------+
