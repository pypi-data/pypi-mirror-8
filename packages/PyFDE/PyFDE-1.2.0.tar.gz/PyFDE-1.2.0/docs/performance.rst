Performance
===========

Great efforts were put to make PyFDE honor the *fast* in its name.

The table below lists the results obtained by *tests/perf.py* compared to
other differential evolution implementation, namely Solver-DE (C++),
lua-de (Lua), and a pure Python 3 version.

All versions were implemented by me, so they all did the same work
(DE/rand/1/bin). The JADE implementation takes twice the time per
iteration, but usually requires a smaller number of iterations to
converge.

+----------------+-----------------+------------+
| Implementation | Total time (ms) | Normalized |
+================+=================+============+
| solver-de      | 42              | 1.00       |
+----------------+-----------------+------------+
| **PyFDE**      | **50**          | **1.19**   |
+----------------+-----------------+------------+
| lua-de (LuaJIT)| 78              | 1.85       |
+----------------+-----------------+------------+
| lua-de (Lua5.1)| 534             | 12.71      |
+----------------+-----------------+------------+
| Pure Python    | 3300            | 78.57      |
+----------------+-----------------+------------+
