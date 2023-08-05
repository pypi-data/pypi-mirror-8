# coding: utf-8

from __future__ import unicode_literals

import unittest

from pymatgen.optimization.linear_assignment import LinearAssignment
import numpy as np

class LinearAssignmentTest(unittest.TestCase):

    def test(self):
        w0 = np.array([[19, 95,  9, 43, 62, 90, 10, 77, 71, 27],
                       [26, 30, 88, 78, 87,  2, 14, 71, 78, 11],
                       [48, 70, 26, 82, 32, 16, 36, 26, 42, 79],
                       [47, 46, 93, 66, 38, 20, 73, 39, 55, 51],
                       [ 1, 81, 31, 49, 20, 24, 95, 80, 82, 11],
                       [81, 48, 35, 54, 35, 55, 27, 87, 96,  7],
                       [42, 17, 60, 73, 37, 36, 79,  3, 60, 82],
                       [14, 57, 23, 69, 93, 78, 56, 49, 83, 36],
                       [11, 37, 24, 70, 62, 35, 64, 18, 99, 20],
                       [73, 11, 98, 50, 19, 96, 61, 73, 98, 14]])
        
        w1 = np.array([[95, 60, 89, 38, 36, 38, 58, 94, 66, 23],
                       [37,  0, 40, 58, 97, 85, 18, 54, 86, 21],
                       [ 9, 74, 11, 45, 65, 64, 27, 88, 24, 26],
                       [58, 90,  6, 36, 17, 21,  2, 12, 80, 90],
                       [33,  0, 74, 75, 11, 84, 34,  7, 39,  0],
                       [17, 61, 94, 68, 27, 41, 33, 86, 59,  2],
                       [61, 94, 36, 53, 66, 33, 15, 87, 97, 11],
                       [22, 20, 57, 69, 15,  9, 15,  8, 82, 68],
                       [40,  0, 13, 61, 67, 40, 29, 25, 72, 44],
                       [13, 97, 97, 54,  5, 30, 44, 75, 16,  0]])
        
        w2 = np.array([[34, 44, 72, 13, 10, 58, 16,  1, 10, 61],
                       [54, 70, 99,  4, 64,  0, 15, 94, 39, 46],
                       [49, 21, 80, 68, 96, 58, 24, 87, 79, 67],
                       [86, 46, 58, 83, 83, 56, 83, 65,  4, 96],
                       [48, 95, 64, 34, 75, 82, 64, 47, 35, 19],
                       [11, 49,  6, 57, 80, 26, 47, 63, 75, 75],
                       [74,  7, 15, 83, 64, 26, 78, 17, 67, 46],
                       [19, 13,  2, 26, 52, 16, 65, 24,  2, 98],
                       [36,  7, 93, 93, 11, 39, 94, 26, 46, 69],
                       [32, 95, 37, 50, 97, 96, 12, 70, 40, 93]])
        
        la0 = LinearAssignment(w0)
        
        self.assertEqual(la0.min_cost, 194, 'Incorrect cost')
        la1 = LinearAssignment(w1)
        self.assertEqual(la0.min_cost, la0.min_cost, 'Property incorrect')
        self.assertEqual(la1.min_cost, 125, 'Incorrect cost')
        la2 = LinearAssignment(w2)
        self.assertEqual(la2.min_cost, 110, 'Incorrect cost')
        
    def test_rectangular(self):
        w0 = np.array([[19, 95,  9, 43, 62, 90, 10, 77, 71, 27],
                       [26, 30, 88, 78, 87,  2, 14, 71, 78, 11],
                       [48, 70, 26, 82, 32, 16, 36, 26, 42, 79],
                       [47, 46, 93, 66, 38, 20, 73, 39, 55, 51],
                       [ 1, 81, 31, 49, 20, 24, 95, 80, 82, 11],
                       [81, 48, 35, 54, 35, 55, 27, 87, 96,  7],
                       [42, 17, 60, 73, 37, 36, 79,  3, 60, 82],
                       [14, 57, 23, 69, 93, 78, 56, 49, 83, 36],
                       [11, 37, 24, 70, 62, 35, 64, 18, 99, 20]])
        la0 = LinearAssignment(w0)
        
        w1 = np.array([[19, 95,  9, 43, 62, 90, 10, 77, 71, 27],
                       [26, 30, 88, 78, 87,  2, 14, 71, 78, 11],
                       [48, 70, 26, 82, 32, 16, 36, 26, 42, 79],
                       [47, 46, 93, 66, 38, 20, 73, 39, 55, 51],
                       [ 1, 81, 31, 49, 20, 24, 95, 80, 82, 11],
                       [81, 48, 35, 54, 35, 55, 27, 87, 96,  7],
                       [42, 17, 60, 73, 37, 36, 79,  3, 60, 82],
                       [14, 57, 23, 69, 93, 78, 56, 49, 83, 36],
                       [11, 37, 24, 70, 62, 35, 64, 18, 99, 20],
                       [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,]])
        la1 = LinearAssignment(w1)
        self.assertEqual(len(la1.solution), 10)
        self.assertEqual(la0.min_cost, la1.min_cost)
        
        self.assertRaises(ValueError, LinearAssignment, w0.T)

    def test_boolean_inputs(self):
        w = np.ones((135,135), dtype=np.bool)
        np.fill_diagonal(w, False)
        la = LinearAssignment(w)
        #if the input doesn't get converted to a float, the masking
        #doesn't work properly
        self.assertEqual(la.orig_c.dtype, np.float64)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
