# test_unit_et.py

from dataclasses import dataclass
from datetime import timezone
from datetime import datetime
import numpy as np
from numpy import random as npr
import pytz
import unittest

import khelio as kh0
from pysolar.solar import get_declination, get_altitude_fast, equation_of_time
from science.wut.enviro import khelio as kh
from test_unit import compareResults, compareResultsNum, printResults

ERR_MARGIN = 0.000_000_000_001  # max error
ERR_ET = 0.51  # max error for test_alt
YR = 2023
NR_TST = 10
TZ = 'Europe/London'
UTC = timezone.utc


class KhelioUnitTestET(unittest.TestCase):

    dnrs = npr.random_integers(1, 366, 366)
    solEts = []
    for dnr in dnrs:
        solEt = equation_of_time(dnr)
        solEts.append(solEt)

    def test_et(self):
        khEts = getEtSeries(kh0.et, self.dnrs)
        # print(f"{self.solEts = }")
        results = compareResults(self.solEts, khEts, err=ERR_ET)
        resultsNum = compareResultsNum(self.solEts, khEts)
        # printResults(results, resultsNum, "test_et")
        self.assertTrue(all(results))

    def test_Et(self):
        khEts = getEtSeries(kh0.Et, self.dnrs)
        results = compareResults(self.solEts, khEts, err=1.5)
        resultsNum = compareResultsNum(self.solEts, khEts)
        # printResults(resultsNum, "test_Et")
        self.assertTrue(all(results))

    # def test_EQT(self):
    #     khEts = getEtSeries(kh0.EQT, self.dnrs)
    #     results = compareResults(self.solEts, khEts, err=35)
    #     resultsNum = compareResultsNum(self.solEts, khEts)
    #     printResults(resultsNum, "test_EQT")
    #     self.assertTrue(all(results))

    def test_Eteq(self):
        khEts = getEtSeries(kh0.Eteq, self.dnrs)
        results = compareResults(self.solEts, khEts, err=1.165)
        resultsNum = compareResultsNum(self.solEts, khEts)
        # printResults(resultsNum, "test_Eteq")
        self.assertTrue(all(results))

    def test_et1(self):
        khEts = getEtSeries(kh0.et1, self.dnrs)
        results = compareResults(self.solEts, khEts, err=0.51)
        resultsNum = compareResultsNum(self.solEts, khEts)
        # printResults(resultsNum, "test_ET1")
        self.assertTrue(all(results))

    def test_et2(self):
        khEts = getEtSeries(kh0.et2, self.dnrs)
        results = compareResults(self.solEts, khEts, err=ERR_MARGIN)
        resultsNum = compareResultsNum(self.solEts, khEts)
        printResults(resultsNum, "test_et2")
        self.assertTrue(all(results))


def getEtSeries(et, dnrs):
    results = []
    for dnr in dnrs:
        results.append(et(dnr))

    return results


if __name__ == '__main__':
    unittest.main(verbosity=2)
