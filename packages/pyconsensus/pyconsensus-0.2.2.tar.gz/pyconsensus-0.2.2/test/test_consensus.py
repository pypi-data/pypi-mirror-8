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

from pyconsensus import Oracle, main

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

    def test_consensus_verbose(self):
        self.oracle = Oracle(votes=self.votes, verbose=True)
        outcome = self.oracle.consensus()
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569613, places=11)

    def test_consensus_weighted(self):
        reputation = np.array([[1], [1], [1], [1], [1], [1]])
        oracle = Oracle(votes=self.votes, reputation=reputation)
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569612, places=11)

    def test_consensus_nans(self):
        votes = np.array([[1, 1, 0, 0],
                          [1, 0, 0, 0],
                          [1, 1, np.nan, 0],
                          [1, 1, 1, 0],
                          [0, 0, 1, 1],
                          [0, 0, 1, 1]])
        oracle = Oracle(votes=votes)
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.28865265952, places=11)

    def test_consensus_weighted_nans(self):
        votes = np.array([[1, 1, 0, 0],
                          [1, 0, 0, 0],
                          [1, 1, np.nan, 0],
                          [1, 1, 1, 0],
                          [0, 0, 1, 1],
                          [0, 0, 1, 1]])
        reputation = np.array([[1], [1], [1], [1], [1], [1]])
        oracle = Oracle(votes=votes, reputation=reputation)
        outcome = oracle.consensus()
        # print(outcome["Agents"]["OldRep"])
        # print(outcome["Agents"]["ThisRep"])
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.28865265952, places=11)

    def test_consensus_scaled(self):
        votes = [[ 0.3, 0.2, 0, 0],
                 [ 0.5, 0.3, 0, 0],
                 [ 0.4, 0.1, 0, 0],
                 [ 0.2, 0.7, 1, 0],
                 [ 0.1, 0.3, 1, 1],
                 [0.15, 0.2, 1, 1]]
        scalar_decision_params = [
            {"scaled": True, "min": 0.1, "max": 0.5},
            {"scaled": True, "min": 0.2, "max": 0.7},
            {"scaled": False, "min": 0, "max": 1},
            {"scaled": False, "min": 0, "max": 1},
        ]
        oracle = Oracle(votes=votes, decision_bounds=scalar_decision_params)
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.362414826111, places=11)

    def test_consensus_scaled_nans(self):
        votes = np.array([[ 0.3, 0.2, 0, 0],
                          [ 0.5, 0.3, np.nan, 0],
                          [ 0.4, 0.1, 0, 0],
                          [ 0.2, 0.7, 1, 0],
                          [ 0.1, 0.3, 1, 1],
                          [0.15, 0.2, 1, 1]])
        scalar_decision_params = [
            {"scaled": True, "min": 0.1, "max": 0.5},
            {"scaled": True, "min": 0.2, "max": 0.7},
            {"scaled": False, "min": 0, "max": 1},
            {"scaled": False, "min": 0, "max": 1},
        ]
        oracle = Oracle(votes=votes, decision_bounds=scalar_decision_params)
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.384073052730, places=11)
        # self.assertAlmostEquals(outcome["Certainty"], 0.362414826111, places=11)

    def test_consensus_weighted_scaled_nans(self):
        votes = np.array([[ 0.3, 0.2, 0, 0],
                          [ 0.5, 0.3, np.nan, 0],
                          [ 0.4, 0.1, 0, 0],
                          [ 0.2, 0.7, 1, 0],
                          [ 0.1, 0.3, 1, 1],
                          [0.15, 0.2, 1, 1]])
        scalar_decision_params = [
            {"scaled": True, "min": 0.1, "max": 0.5},
            {"scaled": True, "min": 0.2, "max": 0.7},
            {"scaled": False, "min": 0, "max": 1},
            {"scaled": False, "min": 0, "max": 1},
        ]
        oracle = Oracle(votes=votes,
                        decision_bounds=scalar_decision_params,
                        reputation=np.array([[1]] * 6))
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.384073052730, places=11)
        # self.assertAlmostEquals(outcome["Certainty"], 0.362414826111, places=11)

    def test_consensus_array(self):
        oracle = Oracle(votes=np.array(self.votes))
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569613, places=11)

    def test_consensus_masked_array(self):
        oracle = Oracle(votes=ma.masked_array(self.votes, np.isnan(self.votes)))
        outcome = oracle.consensus()
        self.assertTrue(0 <= outcome["Certainty"] <= 1)
        self.assertTrue(0 <= outcome["Participation"] <= 1)
        self.assertAlmostEquals(outcome["Certainty"], 0.228237569613, places=11)

    def test_Catch(self):
        expected = [0, 1, 0.5, 0]
        actual = [self.oracle.Catch(0.4),
                  self.oracle.Catch(0.6),
                  Oracle(votes=self.votes, catch_tolerance=0.3).Catch(0.4),
                  Oracle(votes=self.votes, catch_tolerance=0.1).Catch(0.4)]
        self.assertEqual(actual, expected)

    def test_Influence(self):
        expected = [np.array([0.88888889]),
                    np.array([1.33333333]),
                    np.array([1.0]),
                    np.array([1.33333333])]
        actual = self.oracle.Influence(self.oracle.GetWeight(self.c2))
        result = []
        for i in range(len(actual)):
            result.append((actual[i] - expected[i])**2)
        self.assertLess(sum(result), 0.000000000001)

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

    def test_main(self):
        main()
        main(argv=('', '-h'))
        self.assertRaises(main(argv=('', '-q')))

    def tearDown(self):
        del self.votes
        del self.c
        del self.c2
        del self.c3

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConsensus)
    unittest.TextTestRunner(verbosity=2).run(suite)
