#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Consensus mechanism for Augur/Truthcoin.

pyconsensus is a Python implementation of the Augur/Truthcoin consensus
mechanism, described in detail at https://github.com/psztorc/Truthcoin.

Usage:

    from pyconsensus import Oracle

    # Example report matrix:
    #   - each row represents a reporter
    #   - each column represents a event in a prediction market
    my_reports = [[1, 1, 0, 0],
                  [1, 0, 0, 0],
                  [1, 1, 0, 0],
                  [1, 1, 1, 0],
                  [0, 0, 1, 1],
                  [0, 0, 1, 1]]
    my_event_bounds = [
        {"scaled": True, "min": 0.1, "max": 0.5},
        {"scaled": True, "min": 0.2, "max": 0.7},
        {"scaled": False, "min": 0, "max": 1},
        {"scaled": False, "min": 0, "max": 1},
    ]

    oracle = Oracle(reports=my_reports, event_bounds=my_event_bounds)
    oracle.consensus()

"""
from __future__ import division, absolute_import
import sys
import os
import getopt
import json
from pprint import pprint
import numpy as np
import pandas as pd
from weightedstats import weighted_median
from six.moves import xrange as range

__title__      = "pyconsensus"
__version__    = "0.3"
__author__     = "Paul Sztorc and Jack Peterson"
__license__    = "GPL"
__maintainer__ = "Jack Peterson"
__email__      = "jack@tinybike.net"

pd.set_option("display.max_rows", 25)
pd.set_option("display.width", 1000)

np.set_printoptions(linewidth=500,
                    precision=5,
                    suppress=True,
                    formatter={"float": "{: 0.3f}".format})

class Oracle(object):

    def __init__(self, reports=None, event_bounds=None, reputation=None,
                 catch_tolerance=0.1, max_row=5000, alpha=0.1, verbose=False):
        """
        Args:
          reports (list-of-lists): reports matrix; rows = reporters, columns = Events.
          event_bounds (list): list of dicts for each Event
            {
              scaled (bool): True if scalar, False if binary (boolean)
              min (float): minimum allowed value (0 if binary)
              max (float): maximum allowed value (1 if binary)
            }

        """
        self.reports = np.ma.masked_array(reports, np.isnan(reports))
        self.event_bounds = event_bounds
        self.catch_tolerance = catch_tolerance
        self.max_row = max_row
        self.alpha = alpha
        self.verbose = verbose
        self.num_reports = len(reports)
        if reputation is None:
            self.weighted = False
            self.total_rep = self.num_reports
            self.reputation = np.array([1 / float(self.num_reports)] * self.num_reports)
            # print "rep:", self.reputation
            self.rep_coins = (np.copy(self.reputation) * 10**6).astype(int)
            # print "repcoins:", self.rep_coins
            self.total_rep_coins = sum(self.rep_coins)
        else:
            self.weighted = True
            self.total_rep = sum(np.array(reputation).ravel())
            # print "input rep:", reputation
            self.reputation = np.array([i / float(self.total_rep) for i in reputation])
            # self.reputation = reputation
            # print "rep:      ", self.reputation
            self.rep_coins = (np.abs(np.copy(reputation)) * 10**6).astype(int)
            # self.rep_coins = reputation
            # print "repcoins: ", self.rep_coins
            self.total_rep_coins = sum(self.rep_coins)

    def rescale(self):
        """Forces a matrix of raw (user-supplied) information
        (for example, # of House Seats, or DJIA) to conform to
        SVD-appropriate range.

        Practically, this is done by subtracting min and dividing by
        scaled-range (which itself is max-min).

        """
        # Calulate multiplicative factors
        inv_span = []
        for scale in self.event_bounds:
            inv_span.append(1 / float(scale["max"] - scale["min"]))

        # Recenter
        out_matrix = np.ma.copy(self.reports)
        cols = self.reports.shape[1]
        for i in range(cols):
            out_matrix[:,i] -= self.event_bounds[i]["min"]

        # Rescale
        out_matrix[np.isnan(out_matrix)] = np.mean(out_matrix)

        return np.dot(out_matrix, np.diag(inv_span))

    def get_weight(self, v):
        """Takes an array, and returns proportional distance from zero."""
        v = abs(v)
        if np.sum(v) == 0:
            v += 1
        return v / np.sum(v)

    def catch(self, X):
        """Forces continuous values into bins at 0, .5, and 1"""
        if X < 0.5 * (1 - self.catch_tolerance):
            return 0
        elif X > 0.5 * (1 + self.catch_tolerance):
            return 1
        else:
            return .5

    def weighted_cov(self, reports_filled):
        """Weights are the number of coins people start with, so the aim of this
        weighting is to count 1 report for each of their coins -- e.g., guy with 10
        coins effectively gets 10 reports, guy with 1 coin gets 1 report, etc.

        """
        # Compute the weighted mean (of all reporters) for each event
        weighted_mean = np.ma.average(reports_filled,
                                      axis=0,
                                      weights=self.reputation)

        if self.verbose:
            print('=== INPUTS ===')
            print(reports_filled.data)
            print(self.reputation)

            print('=== WEIGHTED MEANS ===')
            print(weighted_mean)

        # Each report's difference from the mean of its event (column)
        mean_deviation = np.matrix(reports_filled - weighted_mean)

        if self.verbose:
            print('=== WEIGHTED CENTERED DATA ===')
            print(mean_deviation)

        # Compute the unbiased weighted population covariance
        # (for uniform weights, equal to np.cov(reports_filled.T, bias=1))
        # covariance_matrix = 1/float(np.sum(self.rep_coins)-1) * np.ma.multiply(mean_deviation.T, self.rep_coins).dot(mean_deviation)
        # ssq = np.sum(self.total_rep_coins**2)
        ssq = np.sum(self.reputation**2)
        covariance_matrix = 1/float(1 - ssq) * np.ma.multiply(mean_deviation.T, self.reputation).dot(mean_deviation)

        if self.verbose:
            print('=== WEIGHTED COVARIANCES ===')
            print(covariance_matrix)

        return covariance_matrix, mean_deviation

    def weighted_prin_comp(self, reports_filled):
        """Principal Component Analysis (PCA) on the reports matrix.

        The reports matrix has reporters as rows and events as columns.

        """
        covariance_matrix, mean_deviation = self.weighted_cov(reports_filled)
        U = np.linalg.svd(covariance_matrix)[0]
        first_loading = U.T[0]
        first_score = np.dot(mean_deviation, U).T[0]

        SVD = np.linalg.svd(covariance_matrix)

        if self.verbose:
            print('=== FROM SINGULAR VALUE DECOMPOSITION OF WEIGHTED COVARIANCE MATRIX ===')
            print(pd.DataFrame(SVD[0].data))
            pprint(SVD[1])
            print(pd.DataFrame(SVD[2].data))

            print('=== FIRST EIGENVECTOR ===')
            print(first_loading)

            print('=== FIRST SCORES ===')
            print(first_score)
            # import pdb; pdb.set_trace()
            # sys.exit(0)

        return first_loading, first_score

    def get_reward_weights(self, reports_filled):
        """Calculates new reputations using a weighted
        Principal Component Analysis (PCA).

        """
        results = self.weighted_prin_comp(reports_filled)
        
        # The first loading (largest eigenvector) is designed to indicate
        # which Events were more 'agreed-upon' than others.
        first_loading = results[0]
        
        # The scores show loadings on consensus (to what extent does
        # this observation represent consensus?)
        first_score = results[1]

        # import pdb; pdb.set_trace()

        # Which of the two possible 'new' reputation vectors had more opinion in common
        # with the original 'old' reputation.
        set1 = first_score + abs(min(first_score))
        set2 = first_score - max(first_score)
        old = np.dot(self.rep_coins.T, reports_filled)
        new1 = np.dot(self.get_weight(set1), reports_filled)
        new2 = np.dot(self.get_weight(set2), reports_filled)

        # Difference in sum of squared errors. If > 0, then new1 had higher
        # errors (use new2); conversely if < 0, then use new1.
        ref_ind = np.sum((new1 - old)**2) - np.sum((new2 - old)**2)
        if ref_ind <= 0:
            adj_prin_comp = set1
        if ref_ind > 0:
            adj_prin_comp = set2
      
        # (set this to uniform if you want a passive diffusion toward equality
        # when people cooperate [not sure why you would]). Instead diffuses towards
        # previous reputation (Smoothing does this anyway).
        row_reward_weighted = self.reputation
        if max(abs(adj_prin_comp)) != 0:
            # Overwrite the inital declaration IFF there wasn't perfect consensus.
            row_reward_weighted = self.get_weight(adj_prin_comp * (self.reputation / np.mean(self.reputation)).T)

        #note: reputation/mean(reputation) is a correction ensuring Reputation is additive. Therefore, nothing can be gained by splitting/combining Reputation into single/multiple accounts.
              
        # Freshly-Calculated Reward (Reputation) - Exponential Smoothing
        # New Reward: row_reward_weighted
        # Old Reward: reputation
        smooth_rep = self.alpha*row_reward_weighted + (1-self.alpha)*self.reputation.T

        return {
            "first_loading": first_loading,
            "old_rep": self.reputation.T,
            "this_rep": row_reward_weighted,
            "smooth_rep": smooth_rep,
        }

    def fill_na(self, reports, scaled_index):
        """Uses existing data and reputations to fill missing observations.
        Essentially a weighted average using all availiable non-NA data.
        """
        reports_new = np.ma.copy(reports)
        if reports.mask.any():
            
            # Our best guess for the Event state (FALSE=0, Ambiguous=.5, TRUE=1)
            # so far (ie, using the present, non-missing, values).
            outcomes_raw = []
            for i in range(reports.shape[1]):
                
                # The Reputation of the rows (players) who DID provide
                # judgements, rescaled to sum to 1.
                active_rep = self.reputation[-reports[:,i].mask]
                active_rep[np.isnan(active_rep)] = 0
                total_active_rep = np.sum(active_rep)
                active_rep /= np.sum(active_rep)

                # The relevant Event with NAs removed.
                # ("What these row-players had to say about the Events
                # they DID judge.")
                active_events = reports[-reports[:,i].mask, i]

                # Guess the outcome; discriminate based on contract type.
                if not scaled_index[i]:
                    outcome_guess = np.dot(active_events, active_rep)                    
                else:
                    outcome_guess = weighted_median(active_events, active_rep)
                outcomes_raw.append(outcome_guess)

            # Fill in the predictions to the original M
            na_mat = reports.mask  # Defines the slice of the matrix which needs to be edited.
            reports_new[na_mat] = 0  # Erase the NA's

            # Slightly complicated:
            NAsToFill = np.dot(na_mat, np.diag(outcomes_raw))
            # This builds a matrix whose columns j:
            #   na_mat was false (the observation wasn't missing) - have a value of Zero
            #   na_mat was true (the observation was missing)     - have a value of the jth element of EventOutcomes.Raw (the 'current best guess')

            reports_new += NAsToFill

            # This replaces the NAs, which were zeros, with the predicted Event outcome.

            # Appropriately force the predictions into their discrete
            # (0,.5,1) slot. (continuous variables can be gamed).
            rows, cols = reports_new.shape
            for i in range(rows):
                for j in range(cols):
                    if not scaled_index[j]:
                        reports_new[i][j] = self.catch(reports_new[i][j])

        return reports_new

    def consensus(self):
        """PCA-based consensus algorithm.

        Returns:
          dict: consensus results

        """
        # Fill the default scales (binary) if none are provided.
        if self.event_bounds is None:
            scaled_index = [False] * self.reports.shape[1]
            scaled_reports = self.reports
        else:
            scaled_index = [scale["scaled"] for scale in self.event_bounds]
            scaled_reports = self.rescale()

        # Handle missing values
        reports_filled = self.fill_na(scaled_reports, scaled_index)

        # Consensus - Row Players
        # New Consensus Reward
        player_info = self.get_reward_weights(reports_filled)
        adj_first_loadings = player_info['first_loading']

        # Column Players (The Event Creators)
        # Calculation of Reward for Event Authors
        # Consensus - "Who won?" Event Outcome    
        # Simple matrix multiplication ... highest information density at reporter_bonus,
        # but need EventOutcomes.Raw to get to that
        outcomes_raw = np.dot(player_info['smooth_rep'], reports_filled).squeeze()

        # Discriminate Based on Contract Type
        for i in range(reports_filled.shape[1]):
            # Our Current best-guess for this Scaled Event (weighted median)
            if scaled_index[i]:
                outcomes_raw[i] = weighted_median(reports_filled[:,i],
                                                  player_info["smooth_rep"].ravel())

        # .5 is obviously undesireable, this function travels from 0 to 1
        # with a minimum at .5
        certainty = abs(2 * (outcomes_raw - 0.5))

        # Grading Authors on a curve.
        consensus_reward = self.get_weight(certainty)

        # How well did beliefs converge?
        avg_certainty = np.mean(certainty)

        # The Outcome (Discriminate Based on Contract Type)
        outcome_adj = []
        for i, raw in enumerate(outcomes_raw):
            outcome_adj.append(self.catch(raw))
            if scaled_index[i]:
                outcome_adj[i] = raw

        outcome_final = []
        for i, raw in enumerate(outcomes_raw):
            outcome_final.append(outcome_adj[i])
            if scaled_index[i]:
                outcome_final[i] *= (self.event_bounds[i]["max"] - self.event_bounds[i]["min"])

        # Participation
        # Information about missing values
        na_mat = self.reports * 0
        na_mat[na_mat.mask] = 1  # indicator matrix for missing

        # Participation Within Events (Columns)
        # % of reputation that answered each Event
        participation_columns = 1 - np.dot(player_info['smooth_rep'], na_mat)

        # Participation Within Agents (Rows)
        # Many options
        # 1- Democracy Option - all Events treated equally.
        participation_rows = 1 - na_mat.sum(axis=1) / na_mat.shape[1]

        # General Participation
        percent_na = 1 - np.mean(participation_columns)

        # Possibly integrate two functions of participation? Chicken and egg problem...
        if self.verbose:
            print('*Participation Information*')
            print('Voter Turnout by question')
            print(participation_columns)
            print('Voter Turnout across questions')
            print(participation_rows)

        # Combine Information
        # Row
        na_bonus_reporters = self.get_weight(participation_rows)
        reporter_bonus = na_bonus_reporters * percent_na + player_info['smooth_rep'] * (1 - percent_na)

        # Column
        na_bonus_events = self.get_weight(participation_columns)
        author_bonus = na_bonus_events * percent_na + consensus_reward * (1 - percent_na)

        return {
            'original': self.reports.data,
            'filled': reports_filled.data,
            'agents': {
                'old_rep': player_info['old_rep'][0],
                'this_rep': player_info['this_rep'][0],
                'smooth_rep': player_info['smooth_rep'][0],
                'na_row': na_mat.sum(axis=1).data.tolist(),
                'participation_rows': participation_rows.data.tolist(),
                'relative_part': na_bonus_reporters.data.tolist(),
                'reporter_bonus': reporter_bonus.data.tolist(),
                },
            'events': {
                'adj_first_loadings': adj_first_loadings.data.tolist(),
                'outcomes_raw': outcomes_raw.data.tolist(),
                'consensus_reward': consensus_reward.data.tolist(),
                'certainty': certainty.data.tolist(),
                'NAs Filled': na_mat.sum(axis=0).data.tolist(),
                'participation_columns': participation_columns.data.tolist(),
                'author_bonus': author_bonus.data.tolist(),
                'outcome_final': outcome_final,
                },
            'participation': 1 - percent_na,
            'certainty': avg_certainty,
        }

def main(argv=None):
    np.set_printoptions(linewidth=500)
    if argv is None:
        argv = sys.argv
    try:
        short_opts = 'hxm'
        long_opts = ['help', 'example', 'missing']
        opts, vals = getopt.getopt(argv[1:], short_opts, long_opts)
    except getopt.GetoptError as e:
        sys.stderr.write(e.msg)
        sys.stderr.write("for help use --help")
        return 2
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(__doc__)
            return 0
        elif opt in ('-x', '--example'):
            # old: true=1, false=0, indeterminate=0.5, no response=-1
            reports = np.array([[  1,  1,  0,  1],
                              [  1,  0,  0,  0],
                              [  1,  1,  0,  0],
                              [  1,  1,  1,  0],
                              [  1,  0,  1,  1],
                              [  0,  0,  1,  1]])
            # new: true=1, false=-1, indeterminate=0.5, no response=0
            reports = np.array([[  1,  1, -1,  1],
                              [  1, -1, -1, -1],
                              [  1,  1, -1, -1],
                              [  1,  1,  1, -1],
                              [  1, -1,  1,  1],
                              [ -1, -1,  1,  1]])
            reputation = [2, 10, 4, 2, 7, 1]
            oracle = Oracle(reports=reports, reputation=reputation)
            pprint(oracle.consensus())
        elif opt in ('-m', '--missing'):
            # old: true=1, false=0, indeterminate=0.5, no response=-1
            reports = np.array([[  1,  1,  0, -1],
                              [  1,  0,  0,  0],
                              [  1,  1,  0,  0],
                              [  1,  1,  1,  0],
                              [ -1,  0,  1,  1],
                              [  0,  0,  1,  1]])
            reports = np.array([[      1,  1,  0, np.nan],
                              [      1,  0,  0,      0],
                              [      1,  1,  0,      0],
                              [      1,  1,  1,      0],
                              [ np.nan,  0,  1,      1],
                              [      0,  0,  1,      1]])
            # new: true=1, false=-1, indeterminate=0.5, no response=0
            reports = np.array([[  1,  1, -1,  0],
                              [  1, -1, -1, -1],
                              [  1,  1, -1, -1],
                              [  1,  1,  1, -1],
                              [  0, -1,  1,  1],
                              [ -1, -1,  1,  1]])
            # new: true=1, false=-1, indeterminate=0.5, no response=np.nan
            reports = np.array([[      1,  1, -1, np.nan],
                              [      1, -1, -1,     -1],
                              [      1,  1, -1,     -1],
                              [      1,  1,  1,     -1],
                              [ np.nan, -1,  1,      1],
                              [     -1, -1,  1,      1]])
            reputation = [2, 10, 4, 2, 7, 1]
            oracle = Oracle(reports=reports, reputation=reputation)
            pprint(oracle.consensus())
        elif opt in ('-t', '--test'):
            reports = np.array([[ 1, 0.5,  0,  0],
                              [ 1, 0.5,  0,  0],
                              [ 1,   1,  0,  0],
                              [ 1, 0.5,  0,  0],
                              [ 1, 0.5,  0,  0],
                              [ 1, 0.5,  0,  0],
                              [ 1, 0.5,  0,  0]])
            

if __name__ == '__main__':
    sys.exit(main(sys.argv))
