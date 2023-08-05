# coding: utf-8

from __future__ import division, unicode_literals

"""
This module contains an algorithm to solve the Linear Assignment Problem
"""


__author__ = "Will Richards"
__copyright__ = "Copyright 2011, The Materials Project"
__version__ = "1.0"
__maintainer__ = "Will Richards"
__email__ = "wrichards@mit.edu"
__date__ = "Jan 28, 2013"

import numpy as np


class LinearAssignment(object):
    """
    This class finds the solution to the Linear Assignment Problem.
    It finds a minimum cost matching between two sets, given a cost
    matrix.

    This class is an implementation of the LAPJV algorithm described in:
    R. Jonker, A. Volgenant. A Shortest Augmenting Path Algorithm for
    Dense and Sparse Linear Assignment Problems. Computing 38, 325-340
    (1987)

    Args:
        costs: The cost matrix of the problem. cost[i,j] should be the
            cost of matching x[i] to y[j]. The cost matrix may be 
            rectangular
        epsilon: Tolerance for determining if solution vector is < 0

    .. attribute: min_cost:

        The minimum cost of the matching

    .. attribute: solution:

        The matching of the rows to columns. i.e solution = [1, 2, 0]
        would match row 0 to column 1, row 1 to column 2 and row 2
        to column 0. Total cost would be c[0, 1] + c[1, 2] + c[2, 0]
    """

    def __init__(self, costs, epsilon=1e-6):
        self.orig_c = np.array(costs, dtype=np.float64)
        self.nx, self.ny = self.orig_c.shape
        self.n = self.ny
        self._inds = np.arange(self.n)

        self.epsilon = abs(epsilon)

        #check that cost matrix is square
        if self.nx > self.ny:
            raise ValueError("cost matrix must have at least as many columns as rows")

        if self.nx == self.ny:
            self.c = self.orig_c
        else:
            self.c = np.zeros((self.n, self.n))
            self.c[:self.nx, :self.ny] = self.orig_c

        #initialize solution vectors
        self._x = np.zeros(self.n, dtype=np.int) - 1
        self._y = self._x.copy()

        #if column reduction doesn't find a solution, augment with shortest
        #paths until one is found
        if self._column_reduction():
            self._augmenting_row_reduction()
            #initialize the reduced costs
            self._update_cred()
            while -1 in self._x:
                self._augment()
        
        self.solution = self._x[:self.nx]
        self._min_cost = None

    @property
    def min_cost(self):
        """
        Returns the cost of the best assignment
        """
        if self._min_cost:
            return self._min_cost

        self._min_cost = np.sum(self.c[np.arange(self.nx), self.solution])
        return self._min_cost

    def _column_reduction(self):
        """
        Column reduction and reduction transfer steps from LAPJV algorithm
        """
        #assign each column to its lowest cost row, ensuring that only row
        #or column is assigned once
        i1, j = np.unique(np.argmin(self.c, axis=0), return_index=True)
        self._x[i1] = j

        #if problem is solved, return
        if len(i1) == self.n:
            return False

        self._y[j] = i1

        #reduction_transfer
        #tempc is array with previously assigned matchings masked
        self._v = np.min(self.c, axis=0)
        tempc = self.c.copy()
        tempc[i1, j] = np.inf
        mu = np.min(tempc[i1, :] - self._v[None, :], axis=1)
        self._v[j] -= mu
        return True

    def _augmenting_row_reduction(self):
        """
        Augmenting row reduction step from LAPJV algorithm
        """
        unassigned = np.where(self._x == -1)[0]
        for i in unassigned:
            while True:
                #find smallest 2 values and indices
                temp = self.c[i] - self._v
                j1 = np.argmin(temp)
                u1 = temp[j1]
                temp[j1] = np.inf
                j2 = np.argmin(temp)
                u2 = temp[j2]

                if u1 < u2:
                    self._v[j1] -= u2 - u1
                elif self._y[j1] != -1:
                    j1 = j2
                k = self._y[j1]
                if k != -1:
                    self._x[k] = -1
                    self._x[i] = j1
                    self._y[j1] = i
                    i = k
                if k == -1 or abs(u1 - u2) < self.epsilon:
                    break

    def _update_cred(self):
        """
        Updates the reduced costs with the values from the
        dual solution
        """
        ui = self.c[self._inds, self._x] - self._v[self._x]
        self.cred = self.c - ui[:, None] - self._v[None, :]

    def _augment(self):
        """
        Finds a minimum cost path and adds it to the matching
        """
        #build a minimum cost tree
        mu, istar, j, _ready, _pred = self._build_tree()

        #update prices
        self._v[_ready] += self._d[_ready] - mu

        #augment the solution with the minimum cost path from the
        #tree. Follows an alternating path along matched, unmatched
        #edges from X to Y
        while True:
            i = _pred[j]
            self._y[j] = i
            k = j
            j = self._x[i]
            self._x[i] = k
            if i == istar:
                break
        self._update_cred()

    def _build_tree(self):
        """
        Builds the tree finding an augmenting path. Alternates along
        matched and unmatched edges between X and Y. The paths are
        stored in _pred (new predecessor of nodes in Y), and
        self._x and self._y
        """
        #find unassigned i*
        istar = np.argmin(self._x)

        #compute distances
        self._d = self.c[istar] - self._v
        _pred = np.zeros(self.n, dtype=np.int) + istar

        #initialize sets
        #READY: set of nodes visited and in the path (whose price gets
        #updated in augment)
        #SCAN: set of nodes at the bottom of the tree, which we need to
        #look at
        #T0DO: unvisited nodes
        _scan = np.zeros(self.n, dtype=np.bool)
        _todo = _scan + True
        _ready = _scan.copy()

        while True:
            #populate scan with minimum reduced distances
            if True not in _scan:
                mu = np.min(self._d[_todo])
                _scan[self._d == mu] = np.True_
                _todo[_scan] = np.False_
                j = np.argmin(self._y * _scan)
                if self._y[j] == -1:
                    return mu, istar, j, _ready, _pred

            #pick jstar from scan (scan always has at least 1)
            _jstar = np.argmax(_scan)

            #pick i associated with jstar
            i = self._y[_jstar]

            _scan[_jstar] = np.False_
            _ready[_jstar] = np.True_

            #find shorter distances
            newdists = mu + self.cred[i, :]
            shorter = np.logical_and(newdists < self._d, _todo)

            #update distances
            self._d[shorter] = newdists[shorter]

            #update predecessors
            _pred[shorter] = i
            for j in np.argwhere(np.logical_and(self._d == mu,
                                       _todo)).flatten():
                if self._y[j] == -1:
                    return mu, istar, j, _ready, _pred
                _scan[j] = np.True_
                _todo[j] = np.False_
