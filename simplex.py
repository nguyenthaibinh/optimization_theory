
# coding: utf-8

# In[124]:

from __future__ import division
import numpy as np
from numpy import *
from fractions import Fraction
 
class Simplex:
 
    def __init__(self, obj):
        self.obj = obj.copy()
        self.rows = []
        self.cons = []
        self.header = []
        for i in range(len(obj)):
            self.header.append("a{}".format(i + 1))
        self.n_vars = len(obj)
        self.op_sol = []
        
        self.op_value = None
        
 
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
        for i in range(0, len(self.obj)-1):
            if self.obj[i] < low:
                low = self.obj[i]
                idx = i
        if idx == -1: return -1
        return idx
 
    def _pivot_row(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        row = -1
        ratio = -1
        for i in range(len(rhs)):
            if (lhs[i] > 0) and (rhs[i] > 0):
                if (ratio < 0) or (ratio > rhs[i] / lhs[i]):
                    row = i
                    ratio = rhs[i] / lhs[i]
                    
        return row
 
    def display(self):
        m = matrix(self.rows)
        k, l = m.shape
        print ("%6s" % " ", end="")
        for i in range(len(self.header)):
            print ("%6s" % self.header[i], end="")
        print ("\n")
        for i in range(k):
            print ("%6s" % " ", end="")
            for j in range(l):
                print ("%6s" % m[i, j], end="")
            print ("\n")
        print ("%6s" % "r", end="")
        for i in range(len(self.obj)):
            print ("%6s" % self.obj[i], end="")
        print ("\n")
 
    def _pivot(self, row, col):
        e = Fraction(self.rows[row][col])
        for i in range(len(self.rows[row])):
            try:
                temp = Fraction(self.rows[row][i]) / Fraction(e)
                self.rows[row][i] = Fraction(temp)
            except:
                print (self.rows[row][i], ";", e)
                pass
        for r in range(len(self.rows)):
            if r == row: continue
            self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
        self.obj = self.obj - self.obj[col]*self.rows[row]
 
    def _check(self):
        if min(self.obj[0:-1]) >= 0:
            return 1
        return 0
    
    def _display_solution(self):
        for i in range(len(self.op_sol)):
            s = "x%d" % (i + 1)
            print ("%6s = %s" % (s, self.op_sol[i]))
        if self.op_value is not None:
            print ("Optimal value:", self.op_value)
         
    def solve(self):
        print ("The initial tableau:")
        # build full tableau
        j = len(self.header) + 1
        for i in range(len(self.rows)):
            self.obj += [0]
            ident = [0 for r in range(len(self.rows))]
            ident[i] = 1
            self.rows[i] += ident + [self.cons[i]]
            self.rows[i] = array(self.rows[i], dtype=Fraction)
            self.header.append("a{}".format(j))
            j = j + 1
        self.header.append("b")
        self.obj = array(self.obj + [0], dtype=Fraction)
 
        # solve
        self.display()
        it = 0
        status = 0
        # status = self._check()
        while status == 0 and (it < 4):
            it = it + 1
            # order the objective function
            obj_cols = np.argsort(self.obj[0: -1])
            col = -1
            row = -1
            for c in obj_cols:
                if self.obj[c] >=0:
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
                status = 0
                print ('pivot column: %s\npivot row: %s\n'%(col + 1 , row + 1))
                self._pivot(row, col)
                self.display()
            elif (col > -1):  # unbounded
                status = -1
            else:  # optimal solution reached
                status = 1
                
        if status == 1:
            print ("The optimal solution is REACHED!")
            print ("Stopping condition is reached")
            for col in range(self.n_vars):
                lhs = [self.rows[i][col] for i in range(len(self.rows))]
                indices = [i for i, x in enumerate(lhs) if x == 1]
                nonzero_indices = [i for i, x in enumerate(lhs) if x != 0]
                if len(indices) > 1:
                    self.op_sol[col].append(0)
                    continue
                elif len(indices) == 1 and len(nonzero_indices) == 1:
                    row = indices[0]
                    self.op_sol.append(self.rows[row][-1])
                else:
                    self.op_sol.append(0)

            self.op_value =  self.obj[-1]
            
            self._display_solution()
            print ("--------------------------------")
        else:
            print ("The solution is UNBOUNDED")
            print ("+++++++++++++++++++++++++")
