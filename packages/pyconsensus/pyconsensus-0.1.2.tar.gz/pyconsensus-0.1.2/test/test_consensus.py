#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Consensus mechanism unit tests.

"""
from __future__ import division, unicode_literals, absolute_import
import os
import sys
import platform
import numpy as np
import numpy.ma as ma
if platform.python_version() < "2.7":
    unittest = __import__("unittest2")
else:
    import unittest
from six.moves import xrange as range

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir))
sys.path.insert(0, os.path.join(HERE, os.pardir, "pyconsensus"))

from pyconsensus import Oracle

class TestConsensus(unittest.TestCase):

    def setUp(self):
        self.votes = [[1, 1, 0, 0],
                      [1, 0, 0, 0],
                      [1, 1, 0, 0],
                      [1, 1, 1, 0],
                      [0, 0, 1, 1],
                      [0, 0, 1, 1]]
        self.oracle = Oracle(votes=self.votes)
        self.c = [1, 2, 3, np.nan, 3]
        self.c2 = ma.masked_array(self.c, np.isnan(self.c))
        self.c3 = [2, 3, -1, 4, 0]

    def test_consensus(self):
        outcome = self.oracle.consensus()
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569613, places=11)

    def test_consensus_array(self):
        self.oracle = Oracle(votes=np.array(self.votes))
        outcome = self.oracle.consensus()
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569613, places=11)

    def test_consensus_masked_array(self):
        self.oracle = Oracle(votes=ma.masked_array(self.votes, np.isnan(self.votes)))
        outcome = self.oracle.consensus()
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569613, places=11)        

    def test_consensus_scaled(self):
        scalar_decision_params = [
            {"scaled": True, "min": 0.1, "max": 0.5},
            {"scaled": True, "min": 0.2, "max": 0.7},
            {"scaled": False, "min": 0, "max": 1},
            {"scaled": False, "min": 0, "max": 1},
        ]
        oracle = Oracle(votes=self.votes, decision_bounds=scalar_decision_params)
        outcome = oracle.consensus()
        self.assertAlmostEquals(outcome["Certainty"], 0.618113325804, places=11)

    def test_WeightedMedian(self):
        data = [
            [7, 1, 2, 4, 10],
            [7, 1, 2, 4, 10],
            [7, 1, 2, 4, 10, 15],
            [1, 2, 4, 7, 10, 15],
            [0, 10, 20, 30],
            [1, 2, 3, 4, 5],
            [30, 40, 50, 60, 35],
            [2, 0.6, 1.3, 0.3, 0.3, 1.7, 0.7, 1.7, 0.4],
        ]
        weights = [
            [1, 1/3, 1/3, 1/3, 1],
            [1, 1, 1, 1, 1],
            [1, 1/3, 1/3, 1/3, 1, 1],
            [1/3, 1/3, 1/3, 1, 1, 1],
            [30, 191, 9, 0],
            [10, 1, 1, 1, 9],
            [1, 3, 5, 4, 2],
            [2, 2, 0, 1, 2, 2, 1, 6, 0],
        ]
        answers = [7, 4, 8.5, 8.5, 10, 2.5, 50, 1.7]
        for datum, weight, answer in zip(data, weights, answers):
            self.assertEqual(self.oracle.WeightedMedian(datum, weight), answer)

    def test_MeanNa(self):
        expected = [1.0, 2.0, 3.0, 2.25, 3.0]
        actual = self.oracle.MeanNa(self.c2)
        self.assertListEqual(list(actual.base), expected)

    def test_Catch(self):
        expected = [0, 1, 0.5, 0]
        actual = [self.oracle.Catch(0.4),
                  self.oracle.Catch(0.6),
                  self.oracle.Catch(0.4, 0.3),
                  self.oracle.Catch(0.4, 0.1)]
        self.assertEqual(actual, expected)

    def test_Influence(self):
        expected = [np.array([0.88888889]),
                    np.array([1.33333333]),
                    np.array([1.]),
                    np.array([1.33333333])]
        actual = self.oracle.Influence(self.oracle.GetWeight(self.c2))
        result = []
        for i in range(len(actual)):
            result.append((actual[i] - expected[i])**2)
        self.assertLess(sum(result), 0.000000000001)

    def test_ReWeight(self):
        self.oracle.MeanNa(self.c2)
        self.oracle.Influence(self.oracle.GetWeight(self.c2))
        expected = [0.08888888888888889,
                    0.17777777777777778,
                    0.26666666666666666,
                    0.2,
                    0.26666666666666666]
        actual = self.oracle.ReWeight(self.c2)
        self.assertListEqual(expected, list(actual.base))

    def test_WeightedPrinComp(self):
        expected = np.array([-0.81674714,
                             -0.35969107,
                             -0.81674714,
                             -0.35969107,
                              1.17643821,
                              1.17643821])
        actual = self.oracle.WeightedPrinComp(self.votes)[1]
        result = []
        for i in range(len(actual)):
            result.append((actual[i] - expected[i])**2)
        self.assertLess(sum(result), 0.000000000001)

    def tearDown(self):
        del self.votes
        del self.c
        del self.c2
        del self.c3

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConsensus)
    unittest.TextTestRunner(verbosity=2).run(suite)
