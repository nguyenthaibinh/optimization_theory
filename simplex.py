from __future__ import division
import numpy as np
from numpy import *
from fractions import Fraction

class Simplex:

    def __init__(self, objective, objective_functions):
        self._objective = objective
        self._objective_function = objective_functions
        self._constraints = {"expressions": [],
                            "types": [],
                            "values": []}
        self._num_vars = 0
        self._num_constrains = 0
        self._tableau = []
        self._tableau_header = []
        self._basis_variables = []
        self._status = 0
        self.optimal_solutions = None
        self.optimal_value = None

    def add_constraint(self, expression, value, constraint_type="="):
        self._num_vars = 0
        if constraint_type in [">=", "<=", "=", ">", "<"]:
            if self._num_vars == 0:
                self._num_vars = len(expression)
            if self._num_vars > 0 and len(expression) != self._num_vars:
                raise ValueError("Length of expressions are not equal!")
            self._num_constrains += 1
            self._constraints['expressions'].append(expression)
            self._constraints['values'].append(value)
            self._constraints['types'].append(constraint_type)

    def _construct_tableau(self):
        num_s_vars = 0  # number of slack and surplus variables

        for constraint_type in self._constraints['types']:
            if constraint_type == '>=':
                num_s_vars += 1

            elif constraint_type == '<=':
                num_s_vars += 1

        total_vars = self._num_vars + num_s_vars

        n_constraints = len(self._constraints['types'])
        tableau = [[Fraction("0/1") for j in range(total_vars + 1)] for i in range(n_constraints + 1)]
        tableau_header = ['x%d' % (i + 1) for i in range(total_vars + 1)]
        tableau_header[-1] = 'b'

        last_idx = self._num_vars

        for i in range(n_constraints):
            constraint = self._constraints['expressions'][i]
            constraint_type = self._constraints['types'][i]
            constraint_val = self._constraints['values'][i]

            tableau[i][:self._num_vars] = constraint[:]

            if constraint_type == '>=' or constraint_type == '>':
                tableau[i][last_idx] = -1
                tableau_header[last_idx] = 's%d' % (last_idx + 1)
                last_idx += 1

            elif constraint_type == '<=' or constraint_type == '<':
                tableau[i][last_idx] = 1
                tableau_header[last_idx] = 's%d' % (last_idx + 1)
                last_idx += 1

            tableau[i][-1] = constraint_val
            tableau[i] = np.array(tableau[i], dtype=Fraction)

        tableau[n_constraints][:self._num_vars] = self._objective_function[:]

        self._tableau = tableau
        self._tableau_header = tableau_header
        self._num_s_vars = num_s_vars

    def construct_tableau(self):
        self._tableau, self._r_rows, self._num_s_vars, self._num_r_vars = self._construct_tableau()
        display_tableau(self._tableau, self._tableau_header)

    def _pivot_column_candidates(self):
        obj = self._tableau[-1]
        ordered_cols = np.argsort(obj[0: -1])
        candidate_cols = []
        for c in ordered_cols:
            if obj[c] < 0:
                candidate_cols.append(c)
        return candidate_cols

    def _pivot_row(self, col):
        n = self._num_constrains
        rhs = [self._tableau[i][-1] for i in range(n)]
        lhs = [self._tableau[i][col] for i in range(n)]
        row = -1
        ratio = -1
        for i in range(len(rhs)):
            if (lhs[i] > 0) and (rhs[i] >= 0):
                if (ratio < 0) or (ratio > rhs[i] / lhs[i]):
                    row = i
                    ratio = rhs[i] / lhs[i]

        return row

    def _get_solutions(self):
        if (self._status == 1):
            n = self._num_constrains
            self.optimal_solutions = [0 for i in range(self._num_vars)]
            rhs = [self._tableau[i][-1] for i in range(n)]
            for col in range(self._num_vars):
                lhs = [self._tableau[i][col] for i in range(n)]
                lhs = np.array(lhs)
                idx = lhs.nonzero()[0]
                if len(idx) == 1 and lhs[idx[0]] == 1:
                    self.optimal_solutions[col] = rhs[idx[0]]
            self.optimal_value = self._tableau[n][-1]

    def _pivot(self, row, col):
        n = self._num_constrains
        e = Fraction(self._tableau[row][col])
        for i in range(len(self._tableau[row])):
            try:
                temp = Fraction(self._tableau[row][i]) / Fraction(e)
                self._tableau[row][i] = Fraction(temp)
            except:
                print(self.rows[row][i], ";", e)
                pass
        for r in range(self._num_constrains):
            if r == row:
                continue
            self._tableau[r] -= self._tableau[r][col] * self._tableau[row]
        self._tableau[n] -= self._tableau[n][col] * self._tableau[row]

    def _check(self):
        if min(self.obj[0:-1]) >= 0:
            return 1
        return 0

    def _display_solution(self):
        for i in range(len(self.optimal_solutions)):
            s = "x%d" % (i + 1)
            print("%6s = %s" % (s, self.optimal_solutions[i]))
        if self.optimal_value is not None:
            print("Optimal value:", self.optimal_value)

    def solve(self):
        self._construct_tableau()
        display_tableau(self._tableau, self._tableau_header,
                        message="The initial tableau:")

        it = 0

        while self._status == 0 and it < 4:
            it += 1
            cols = self._pivot_column_candidates()
            p_row = -1
            p_col = -1

            if len(cols) == 0:
                self._status = 1
            else:
                for c in cols:
                    r = self._pivot_row(c)
                    if r < 0:
                        self._status = -1
                        continue
                    else:
                        p_col = c
                        p_row = r
                        self._status = 0
                        break
            if (self._status == 0):
                print("pivot_column: %d" % (p_col + 1))
                print("pivot_row: %d" % (p_row + 1))
                self._pivot(p_row, p_col)
                display_tableau(self._tableau, self._tableau_header)
            elif (self._status == 1):
                print("Optimal reached!")
                self._get_solutions()
                self._display_solution()
            else:
                print("Unbounded")


def display_tableau(tableau, tableau_header, message=None):
    if message:
        print(message)
    n_rows = len(tableau)
    n_cols = len(tableau_header)
    print("%3s" % " ", end="")
    for i in range(n_cols):
        print("%6s" % tableau_header[i], end="")
    print("\n")
    for i in range(0, n_rows):
        if i == (n_rows - 1):
            print("%3s" % "r", end="")
        else:
            print("%3s" % " ", end="")
        for j in range(len(tableau[i])):
            print("%6s" % tableau[i][j], end="")
        print("\n")
