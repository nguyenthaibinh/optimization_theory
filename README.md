## The source code for one-phase simplex method and two-phase simplex method

This is a library written in Python for the simplex method in Linear Programming. The library includes one-phase simplex and two-phase simplex method.

The library can solve the linear pramming problem with mixed constraints.

### File structure:
- **simplex.py**: the implementation of one-phase simplex class
- **simplex2.py**: the implementation of two-phase simplex class
- **test_simplex.py**, **test_simplex2.py**: the script to test the library
- **test_simplex.ipynb**, **test_simplex2.ipynb**: the test results in jupyter notebook

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

#### Two-phase simplex method
```python
from two_phase_simplex import Simplext

t = sp2.Simplex2("min", [-3, -1, -3])
t.add_constraint([2, 1, 1], 2, ">=")
t.add_constraint([1, 1, 3], 5, "<=")
t.add_constraint([2, 2, 1], 6, "=")
t.solve()
```

### Requirements
Python 3.x with **numpy** library installed.

### Some examples:
- Example using both one-phase simplex and two-phase simplex
https://github.com/nguyenthaibinh/optimization_theory/blob/master/test_simplex.ipynb

- An example that one-phase simplex method CANNOT solve but two-phase simplex method CAN solve
https://github.com/nguyenthaibinh/optimization_theory/blob/master/test_simplex2.ipynb
  
