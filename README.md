---
Title: README
layout: page
markdown: kramdown
kramdown:
  input: GFM
---
## The source code for one-phase simplex method and two-phase simplex method

This is a library written in Python for the simplex method in Linear Programming. The library includes one-phase simplex and two-phase simplex method.

The library can solve the linear pramming problem with mixed constraints, i.e., in the following form:

$min z = c_1x_1$

### File structure:
- simplex.py: the implementation of one-phase simplex class
- two_phase_simplex.py: the implementation of two-phase simplex class
