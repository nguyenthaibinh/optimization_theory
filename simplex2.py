from __future__ import division
import numpy as np
from numpy import *
from fractions import Fraction

class Simplex2:
    def __init__(self, objective, objective_function):
        self._objective = objective
        self._objective_function = objective_function
        self._constraints = {"expressions": [],
                            "types": [],
                            "values": []}
        self._num_vars = 0
        self._num_constraints = 0
        self._tableau = []
        self._tableau_header = []
        self._basis_variables = []
        self._status = 0
        self.optimal_solutions = None
        self.optimal_value = None
        self._basic_rows = None

    def add_constraint(self, expression, value, constraint_type="="):
        self._num_vars = 0
        if constraint_type in [">=", "<=", "=", ">", "<"]:
            if self._num_vars == 0:
                self._num_vars = len(expression)
            if self._num_vars > 0 and len(expression) != self._num_vars:
                raise ValueError("Length of expressions are not equal!")
            self._num_constraints += 1
            self._constraints['expressions'].append(expression)
            self._constraints['values'].append(value)
            self._constraints['types'].append(constraint_type)

    def _construct_tableau(self):
        num_s_vars = 0  # number of slack and surplus variables
        num_r_vars = 0  # number of additional variables to balance equality and less than equal to

        for constraint_type in self._constraints['types']:
            if constraint_type == '>=' or constraint_type == '>':
                num_s_vars += 1
                num_r_vars += 1

            elif constraint_type == '<=' or constraint_type == '<':
                num_s_vars += 1

            elif constraint_type == '=':
                num_r_vars += 1

        total_vars = self._num_vars + num_s_vars + num_r_vars

        n_cons = self._num_constraints
        tableau = [[Fraction("0/1") for j in range(total_vars + 1)]
        			for i in range(n_cons + 1)]
        tableau_header = ['x%d' % (i + 1) for i in range(total_vars + 1)]
        tableau_header[-1] = 'b'

        r_rows = []
        basic_rows = dict()
        last_idx = self._num_vars

        for i in range(n_cons):
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
                tableau[n_cons][last_idx] = 1
                basic_rows[i] = last_idx
                tableau[n_cons][last_idx] = 1
                last_idx += 1

        for i in range(n_cons):
            constraint = self._constraints['expressions'][i]
            constraint_type = self._constraints['types'][i]
            constraint_val = self._constraints['values'][i]

            tableau[i][:self._num_vars] = constraint[:]

            if constraint_type == '>=' or constraint_type == '>':
                tableau[i][last_idx] = 1
                tableau_header[last_idx] = 'r%d' % (last_idx + 1)
                tableau[n_cons][last_idx] = 1
                basic_rows[i] = last_idx
                last_idx += 1
                r_rows.append(i)

            elif constraint_type == '=':
                tableau[i][last_idx] = 1
                tableau_header[last_idx] = 'r%d' % (last_idx + 1)
                tableau[n_cons][last_idx] = 1
                basic_rows[i] = last_idx
                last_idx += 1
                r_rows.append(i)

            tableau[i][-1] = constraint_val
            tableau[i] = np.array(tableau[i], dtype=Fraction)

        tableau[n_cons] = np.array(tableau[n_cons], dtype=Fraction)

        self._tableau = tableau
        self._tableau_header = tableau_header
        self._r_rows = r_rows
        self._basic_rows = basic_rows
        self._num_s_vars = num_s_vars
        self._num_r_vars = num_r_vars

    def _construct_phase2_tableau(self):
        n_vars = self._num_vars + self._num_s_vars
        n_cons = self._num_constraints
        tableau = [[Fraction(0, 1) for c in range(n_vars + 1)]
                   for r in range(n_cons + 1)]
        tableau_header = ['x%d' % (c + 1) for c in range(n_vars + 1)]
        for c in range(self._num_vars, n_vars):
            tableau_header[c] = 's%d' % (c + 1)
        tableau_header[-1] = 'b'

        for r in range(n_cons):
            tableau[r][:n_vars] = self._tableau[r][:n_vars]
            tableau[r][-1] = self._tableau[r][-1]
            tableau[r] = np.array(tableau[r], dtype=Fraction)
        tableau[n_cons][:self._num_vars] = self._objective_function[:]
        tableau[n_cons][-1] = self._tableau[n_cons][-1]
        tableau[n_cons] = np.array(tableau[n_cons], dtype=Fraction)

        self._tableau = tableau
        self._tableau_header = tableau_header
        
        keys = list(self._basic_rows.keys())
        for key in keys:
            if self._basic_rows[key] >= n_vars:
                del self._basic_rows[key]

    def _pivot_column_candidates(self):
        obj = self._tableau[-1]
        ordered_cols = np.argsort(obj[0: -1])
        candidate_cols = []
        for c in ordered_cols:
            if obj[c] < 0:
                candidate_cols.append(c)
        return candidate_cols

    def _pivot_row(self, col):
        n = self._num_constraints
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
            n = self._num_constraints
            n_vars = self._num_vars + self._num_s_vars
            self.optimal_solutions = [0 for i in range(n_vars)]
            rhs = [self._tableau[i][-1] for i in range(n)]
            for col in range(n_vars):
                lhs = [self._tableau[i][col] for i in range(n)]
                lhs = np.array(lhs)
                idx = lhs.nonzero()[0]
                if len(idx) == 1 and lhs[idx[0]] == 1:
                    self.optimal_solutions[col] = rhs[idx[0]]
            self.optimal_value = self._tableau[n][-1]

    def _pivot(self, row, col):
        n = self._num_constraints
        e = Fraction(self._tableau[row][col])
        for i in range(len(self._tableau[row])):
            try:
                temp = Fraction(self._tableau[row][i]) / Fraction(e)
                self._tableau[row][i] = Fraction(temp)
                self._basic_rows[row] = col
            except:
                print(self.rows[row][i], ";", e)
                pass
        for r in range(self._num_constraints):
            if r == row:
                continue
            self._tableau[r] -= self._tableau[r][col] * self._tableau[row]
        self._tableau[n] -= self._tableau[n][col] * self._tableau[row]

    def _check(self):
        if min(self.obj[0:-1]) >= 0:
            return 1
        return 0

    def _display_solution(self, phase=1):
        if phase == 1:
            n_vars = len(self.optimal_solutions)
        else:
            n_vars = self._num_vars
        for i in range(n_vars):
            s = self._tableau_header[i]
            print("%6s = %s" % (s, self.optimal_solutions[i]))
        if phase == 2 and self.optimal_value is not None:
            print("Optimal value:", self.optimal_value)

    def _phase_1(self):
        self._construct_tableau()
        display_tableau(self._tableau, self._tableau_header,
                        mess="PHASE 1\n========\nThe initial tableau:")
        self._make_zero_basis_variables()
        display_tableau(self._tableau, self._tableau_header,
                        mess="Make zero under the basis variables, we get:")
        self._solve()
        return 0

    def _phase_2(self):
        if self._status == -1:
            print("Can not perform phase 2 because phase 1 is infeasible")
            return
        elif self._status == 0:
            print("Phase 1 has not been performed yet. Perform phase 1 first!")

        self._construct_phase2_tableau()
        display_tableau(self._tableau, self._tableau_header,
                        mess="PHASE 2\n========\nRemove artificial variables, we get:")

        self._make_zero_basis_variables()
        display_tableau(self._tableau, self._tableau_header,
                        mess="Make zero under the basis variables, we get:")
        self._solve()

    def _make_zero_basis_variables(self):
        n = self._num_constraints
        for row, col in self._basic_rows.items():
            self._tableau[n] = self._tableau[n] - self._tableau[n][col] * self._tableau[row]
        return 0

    def _solve(self):
        it = 0
        self._status = 0
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
                print("pivot_row: %d\n" % (p_row + 1))
                self._pivot(p_row, p_col)
                display_tableau(self._tableau, self._tableau_header)
            elif (self._status == 1):
                print("Optimal reached!")
                self._get_solutions()
                # self._display_solution()
            else:
                print("Unbounded")

    def solve(self):
        self._phase_1()
        if self._status == 1:
            self._display_solution(phase=1)
        self._phase_2()
        if self._status == 1:
            self._display_solution(phase=2)


def display_tableau(tableau, tableau_header, mess=None):
    if mess:
        print("\n%s\n" % mess)
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
