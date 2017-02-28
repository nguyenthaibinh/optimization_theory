## The source code for one-phase simplex method and two-phase simplex method

This is a library written in Python for the simplex method in Linear Programming. The library includes one-phase simplex and two-phase simplex method.

The library can solve the linear pramming problem with mixed constraints.

### File structure:
- simplex.py: the implementation of one-phase simplex class
- two_phase_simplex.py: the implementation of two-phase simplex class

### Usage:

#### One-phase simplex
```python

from simplex import Simplex

t = sp.Simplex("min", [-3, -1, -3])
t.add_constraint([2, 1, 1], 2, ">=")
t.add_constraint([1, 1, 3], 5, "<=")
t.add_constraint([2, 2, 1], 6, "=")
t.solve()

```
Result:
```
The initial tableau:
       x1    x2    x3    s4    s5     b

        2     1     1    -1     0     2

        1     1     3     0     1     5

        2     2     1     0     0     6

  r    -3    -1    -3     0     0     0

pivot_column: 1
pivot_row: 1
       x1    x2    x3    s4    s5     b

        1   1/2   1/2  -1/2     0     1

        0   1/2   5/2   1/2     1     4

        0     1     0     1     0     4

  r     0   1/2  -3/2  -3/2     0     3

pivot_column: 3
pivot_row: 2
       x1    x2    x3    s4    s5     b

        1   2/5     0  -3/5  -1/5   1/5

        0   1/5     1   1/5   2/5   8/5

        0     1     0     1     0     4

  r     0   4/5     0  -6/5   3/5  27/5

pivot_column: 4
pivot_row: 3
       x1    x2    x3    s4    s5     b

        1     1     0     0  -1/5  13/5

        0     0     1     0   2/5   4/5

        0     1     0     1     0     4

  r     0     2     0     0   3/5  51/5

Optimal reached!
    x1 = 13/5
    x2 = 0
    x3 = 4/5
Optimal value: 51/5
```

#### Two-phase simplex method
```python
from two_phase_simplex import Simplext
t = sp2.Simplex2("min", [-3, -1, -3])
t.add_constraint([2, 1, 1], 2, ">=")
t.add_constraint([1, 1, 3], 5, "<=")
t.add_constraint([2, 2, 1], 6, "=")
t.solve()
```
Result:
```
PHASE 1
========
The initial tableau:

       x1    x2    x3    s4    s5    r6    r7     b

        2     1     1    -1     0     1     0     2

        1     1     3     0     1     0     0     5

        2     2     1     0     0     0     1     6

  r     0     0     0     0     0     1     1     0


Make zero under the basis variables, we get:

       x1    x2    x3    s4    s5    r6    r7     b

        2     1     1    -1     0     1     0     2

        1     1     3     0     1     0     0     5

        2     2     1     0     0     0     1     6

  r    -4    -3    -2     1     0     0     0    -8

pivot_column: 1
pivot_row: 1

       x1    x2    x3    s4    s5    r6    r7     b

        1   1/2   1/2  -1/2     0   1/2     0     1

        0   1/2   5/2   1/2     1  -1/2     0     4

        0     1     0     1     0    -1     1     4

  r     0    -1     0    -1     0     2     0    -4

pivot_column: 2
pivot_row: 1

       x1    x2    x3    s4    s5    r6    r7     b

        2     1     1    -1     0     1     0     2

       -1     0     2     1     1    -1     0     3

       -2     0    -1     2     0    -2     1     2

  r     2     0     1    -2     0     3     0    -2

pivot_column: 4
pivot_row: 3

       x1    x2    x3    s4    s5    r6    r7     b

        1     1   1/2     0     0     0   1/2     3

        0     0   5/2     0     1     0  -1/2     2

       -1     0  -1/2     1     0    -1   1/2     1

  r     0     0     0     0     0     1     1     0

Optimal reached!
    x1 = 0
    x2 = 3
    x3 = 0
    s4 = 1
    s5 = 2

PHASE 2
========
Remove artificial variables, we get:

       x1    x2    x3    s4    s5     b

        1     1   1/2     0     0     3

        0     0   5/2     0     1     2

       -1     0  -1/2     1     0     1

  r    -3    -1    -3     0     0     0


Make zero under the basis variables, we get:

       x1    x2    x3    s4    s5     b

        1     1   1/2     0     0     3

        0     0   5/2     0     1     2

       -1     0  -1/2     1     0     1

  r    -2     0  -5/2     0     0     3

pivot_column: 3
pivot_row: 2

       x1    x2    x3    s4    s5     b

        1     1     0     0  -1/5  13/5

        0     0     1     0   2/5   4/5

       -1     0     0     1   1/5   7/5

  r    -2     0     0     0     1     5

pivot_column: 1
pivot_row: 1

       x1    x2    x3    s4    s5     b

        1     1     0     0  -1/5  13/5

        0     0     1     0   2/5   4/5

        0     1     0     1     0     4

  r     0     2     0     0   3/5  51/5

Optimal reached!
    x1 = 13/5
    x2 = 0
    x3 = 4/5
Optimal value: 51/5
```
