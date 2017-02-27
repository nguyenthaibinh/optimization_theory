
# coding: utf-8

# In[142]:

from __future__ import division
import numpy as np
from numpy import *
from fractions import Fraction


class TwoPhasesSimplex:

    def __init__(self, obj):
        self.obj = []
        self.original_obj = []
        self.phase_1_rows = None
        for i in range(len(obj)):
            self.obj += [0]
            self.original_obj += [obj[i]]
        self.rows = []
        self.cons = []
        self.header = []
        for i in range(len(obj)):
            self.header.append("a{}".format(i + 1))
        self.n_vars = len(obj)
        self.op_sol = []

        self.op_value = None
        self.status = 0

    def add_constraint(self, expression, value):
        # self.rows.append([0] + expression)
        self.rows.append(expression)
        self.cons.append(value)

    def _pivot_column(self):
        """
        find the pivot column
        """
        low = 0
        idx = -1
        for i in range(0, len(self.obj) - 1):
            if self.obj[i] < low:
                low = self.obj[i]
                idx = i
        if idx == -1:
            return -1
        return idx

    def _pivot_row(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        row = -1
        ratio = -1
        for i in range(len(rhs)):
            if (lhs[i] > 0) and (rhs[i] >= 0):
                if (ratio < 0) or (ratio > rhs[i] / lhs[i]):
                    row = i
                    ratio = rhs[i] / lhs[i]

        return row

    def display(self):
        m = matrix(self.rows)
        n_rows, n_cols = m.shape
        print(" %6s" % " ", end="")
        for i in range(len(self.header)):
            print(" %6s" % self.header[i], end="")
        print("\n")
        for i in range(n_rows):
            print(" %6s" % " ", end="")
            for j in range(n_cols):
                print(" %6s" % m[i, j], end="")
            print("\n")
        print(" %6s" % "r", end="")
        for i in range(len(self.obj)):
            print(" %6s" % self.obj[i], end="")
        print("\n")

    def _pivot(self, row, col):
        e = Fraction(self.rows[row][col])
        self.rows[row] /= e
        for r in range(len(self.rows)):
            if r == row:
                continue
            self.rows[r] = self.rows[r] - self.rows[r][col] * self.rows[row]
        self.obj = self.obj - self.obj[col] * self.rows[row]

    def _check(self):
        if min(self.obj[0:-1]) >= 0:
            return 1
        return 0

    def _display_solution(self, mess="Optimal solution:", display_val=False):
        if self.status != 1:
            return
        print(mess)
        for i in range(self.n_vars):
            s = "x%d" % (i + 1)
            print(" %6s = %s" % (s, self.op_sol[i]))
        if self.op_value is not None and display_val:
            print("Optimal value:", self.op_value)

    def _phase_1(self):
        print("PERFORM PHASE 1:")
        self._initialize_tableau_phase_1()
        self.display()
        self._update_phase_1_tableau()
        self.display()
        self._solve()
        self._display_solution(mess="Optimal solution of the phase 1:")

    def _phase_2(self):
        print("\n\n================")
        print("PERFORM PHASE 2:")
        # build full tableau

        # solve
        self._initialize_tableau_phase_2()
        self.display()
        self._update_phase_2_tableau()
        self.display()

        self._solve()
        self._display_solution(display_val=True)

    def _initialize_tableau_phase_1(self):
        print("   The initial tableau of phase 1.")
        j = len(self.header) + 1
        for i in range(len(self.rows)):
            self.obj += [1]
            ident = [0 for r in range(len(self.rows))]
            ident[i] = 1
            self.rows[i] += ident + [self.cons[i]]
            self.rows[i] = array(self.rows[i], dtype=Fraction)
            self.header.append("a{}".format(j))
            j = j + 1
        self.header.append("b")
        self.obj = array(self.obj + [0], dtype=Fraction)

    def _initialize_tableau_phase_2(self):
        phase_1_rows = self.rows.copy()
        n_rows = len(self.rows)
        self.rows = []
        for i in range(n_rows):
            self.rows.append(list(phase_1_rows[i][0:self.n_vars]))
            self.rows[i].append(phase_1_rows[i][-1])
            self.rows[i] = array(self.rows[i], dtype=Fraction)
        self.obj = self.original_obj.copy()
        self.obj = array(self.obj + [0], dtype=Fraction)
        self.header = []
        for i in range(self.n_vars):
            self.header.append("a%d" % (i + 1))
        self.header.append("b")

    def _update_phase_1_tableau(self):
        print("Make the last row zero under the basis variables:")
        # print("self.rows len:", len(self.rows[0]))
        # print("self.obj[0:-1]:", len(self.obj[0:-1]))
        self.obj = -np.sum(self.rows, axis=0)
        self.obj[self.n_vars:-1] = 0
        # self.obj[-1] = np.sum(self.cons)

    def _update_phase_2_tableau(self):
        print("Make the last row zero under the basis variables:")
        for col in range(self.n_vars):
            lhs = [self.rows[i][col] for i in range(len(self.rows))]
            indices = [i for i, x in enumerate(lhs) if x == 1]
            if len(indices) > 1:
                self.op_sol[col].append(0)
                continue
            if len(indices) == 1:
                row = indices[0]
                self.obj = self.obj - self.obj[col] * self.rows[row]

    def _solve(self):
        it = 0
        self.status = 0
        # status = self._check()
        while self.status == 0 and (it < 4):
            it = it + 1
            # order the objective function
            obj_cols = np.argsort(self.obj[0: -1])
            col = -1
            row = -1
            for c in obj_cols:
                if self.obj[c] >= 0:
                    break
                col = c
                r = self._pivot_row(c)
                if r == -1:
                    continue
                col = c
                row = r
                break
            # c = self._pivot_column()
            if (row > -1) and (col > -1):  # if there exists a pivot item
                self.status = 0
                print('pivot column: %s\npivot row: %s\n' % (col + 1, row + 1))
                self._pivot(row, col)
                self.display()
            elif (col > -1):  # unbounded
                self.status = -1
            else:  # optimal solution reached
                self.status = 1

        if self.status == 1:
            for col in range(self.n_vars):
                lhs = [self.rows[i][col] for i in range(len(self.rows))]
                indices = [i for i, x in enumerate(lhs) if x == 1]
                if len(indices) > 1:
                    self.op_sol[col].append(0)
                    continue
                if len(indices) == 1:
                    row = indices[0]
                    self.op_sol.append(self.rows[row][-1])
                else:
                    self.op_sol.append(0)

            self.op_value = self.obj[-1]
        else:
            print("The solution is UNBOUNDED")
            print("+++++++++++++++++++++++++")

        return self.status

    def solve(self):
        self._phase_1()
        self._phase_2()
