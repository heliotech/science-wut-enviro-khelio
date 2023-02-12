# test_unit.py

from dataclasses import dataclass
from datetime import timezone
from datetime import datetime
import numpy as np
from numpy import random as npr
import pytz
import unittest

import khelio as kh0
from pysolar.solar import get_declination, get_altitude_fast, get_azimuth_fast
from science.wut.enviro import khelio as kh

ERR_MARGIN = 0.000_000_000_001  # max error
ERR_ALT = 0.1  # max error for test_alt
YR = 2023
NR_TST = 10
TZ = 'Europe/London'
UTC = timezone.utc


class KhelioUnitTest(unittest.TestCase):

    def test_dayNr(self):
        dates = []
        for i in range(NR_TST):
            m, d = getRanDate()
            dates.append((m, d))
            dnr0 = int(datetime(YR, m, d).strftime("%-j"))
            dnr1 = kh.dayNr(m, d)
            # print(f"{dnr0 = } vs. {dnr1} = dnr1")
            self.assertEqual(dnr0, dnr1)
        # dates = [(2, 9), (2, 28), (9, 30)]
        results0 = [int(datetime(YR, m, d).strftime("%-j")) for (m, d)
                    in dates]
        # print(f"{results0 = }")
        results1 = kh.dayNr(dates)
        # self.assertEqual(results0, results1)
        self.assertTrue(all([d0 == d1 for (d0, d1) in
                             zip(results0, results1)]))

    def test_inc(self):
        args = [getINCArgs() for _ in range(NR_TST)]
        INC0 = [kh0.inc(*vals) for vals in args]
        INC1 = [kh.inc(*vals) for vals in args]
        results = [abs(i0 - i1) < ERR_MARGIN for (i0, i1) in zip(INC0, INC1)]
        # print(f"test_inc {results = }, {all(results) = }")
        self.assertTrue(all(results))

    def test_dec(self):
        DECS0 = []
        DECS1 = []
        for i in range(NR_TST):
            m, d = getRanDate()
            dnr = kh.dayNr(m, d)
            DECS0.append(get_declination(dnr))
            DECS1.append(kh.dec(dnr))
        results = [abs(d0 - d1) < ERR_MARGIN for (d0, d1) in zip(DECS0, DECS1)]
        # print(f"test_dec {results = }")
        self.assertTrue(all(results))

    def test_alt(self):
        ALTS0 = []
        ALTS1 = []
        for i in range(NR_TST):
            glt = GeoLocTime(LON=0, LONStd=0)
            dttm = glt.dttm
            ALTS0.append(get_altitude_fast(glt.LAT, -glt.LON, dttm))
            # ALTS0.append(kh0.alt(glt.DEC, glt.LAT, glt.HRA))
            dHRA = glt.et*(15/60)
            ALTS1.append(kh.alt(glt.DEC, glt.LAT, glt.HRA + dHRA))
            # get_altitude_fast(latitude_deg, longitude_deg, when)
        results = compareResults(ALTS0, ALTS1, err=ERR_ALT)
        resultsNum = compareResultsNum(ALTS0, ALTS1)
        print(f"test_alt, {results = }, {all(results) = }")
        print(f"test_alt, {resultsNum = }, {np.mean(resultsNum) = :.5f}, "
              f"{np.median(resultsNum) = :.5f}, "
              f"(max, min) = ({max(resultsNum):.5f}, {min(resultsNum):.5f})")
        self.assertTrue(all(results))

    def test_azi(self):
        AZIS0 = []
        AZIS1 = []
        for i in range(NR_TST):
            glt = GeoLocTime(LON=0, LONStd=0)
            dttm = glt.dttm
            AZIS0.append(get_azimuth_fast(glt.LAT, glt.LON, dttm))
            # ALTS0.append(kh0.alt(glt.DEC, glt.LAT, glt.HRA))
            dHRA = glt.et*(15/60)
            AZIS1.append(kh0.azi(glt.DEC, glt.LAT, glt.HRA + dHRA))
            # get_altitude_fast(latitude_deg, longitude_deg, when)
        results = compareResults(AZIS0, AZIS1, err=ERR_ALT)
        resultsNum = compareResultsNum(AZIS0, AZIS1)
        # print(f"test_azi, {results = }, {all(results) = }")
        # print(f"test_azi, {resultsNum = }, {np.mean(resultsNum) = :.5f}, "
        #       f"{np.median(resultsNum) = :.5f}, "
        #       f"(max, min) = ({max(resultsNum):.5f}, {min(resultsNum):.5f})")
        printResults(resultsNum, "test_azi")
        self.assertTrue(all(results))


def printResults(resultsNum, src=""):
    print(f"{src}: {'[' + ', '.join(f'{v:.5f}' for v in resultsNum) + ']'}, "
          f"{np.mean(resultsNum) = :.5f}, "
          f"{np.median(resultsNum) = :.5f}, "
          f"(max, min) = ({max(resultsNum):.5f}, {min(resultsNum):.5f})")


def compareResults(vals0, vals1, err=ERR_MARGIN):
    """Results comparison"""

    results = [abs(v0 - v1) < err for (v0, v1) in zip(vals0, vals1)]
    return results


def compareResultsNum(vals0, vals1):
    """Results comparison, numerical"""

    results = [abs(v0 - v1) for (v0, v1) in zip(vals0, vals1)]
    return results


def getINCArgs():
    """Calculating random tuple of args. for inc"""

    DEC = getRandDEC()
    LAT = getRandLAT()
    TIL = getRandTIL()
    ORI = getRandORI()
    HRA = getRandHRA()

    return DEC, LAT, TIL, ORI, HRA


def getRandDECLATHRA():
    """Random arguments in the form of (DEC, LAT, HRA) """

    DEC = getRandDEC()
    LAT = getRandLAT()
    HRA = getRandHRA()

    return DEC, LAT, HRA


def getRandSign():
    """Calculating random (-1, 1)"""

    sval = npr.random(1)[0]
    return -1 if sval < 0.5 else 1


def getRanDate():
    """Calculating a random date"""

    m = npr.randint(1, 12)
    d = npr.randint(1, 28)
    return m, d


def getRandDEC():
    m, d = getRanDate()
    dnr = kh.dayNr(m, d)
    return get_declination(dnr)


def getRandLAT(l0=23.5, l1=66):
    """ Getting random, 'safe' LAT """

    dl = l1-l0
    r = npr.random(1)[0]

    return r*dl + l0


def getRandLON():
    """ Getting random, 'safe' LAT """

    r = npr.random(1)[0]
    sign = getRandSign()

    return r*180*sign


def getRandTIL(l0=0, l1=90):
    """Calculating random tilt angle"""

    dl = l1 - l0
    r = npr.random(1)[0]

    return r*dl + l0


def getRandORI(l0=0, l1=359.999):
    """Calculating random orientation angle"""

    dl = l1 - l0
    r = npr.random(1)[0]

    return r*dl + l0 - 180  # !!!


def getRandHRA():
    """Calculating random hour angle"""

    sign = getRandSign()
    r = npr.random(1)[0]*180

    return r*sign


@dataclass
class GeoLocTime:
    """Class for 'random' DEC, LAT, LON, HRA """

    def __init__(self, LON=None, LONStd=None, tz=UTC):
        m, d = getRanDate()
        self.m, self.d = m, d
        dnr = int(datetime(YR, m, d).strftime("%-j"))
        # tzinfo = pytz.timezone(tz)
        HRA_ = getRandHRA()  # HRA raw, unaware of tz
        AST = kh0.ast1(kh0.tau(HRA_), dnr, LON, LONStd, teq=kh0.ET2)
        self.AST = AST
        HRA = 0  # qfix  # kh.hra(AST)
        self.HRA = HRA
        h_ = kh.hr(HRA)
        h, mn, s = kh.timeDec2HMS(h_)
        # print(f"D: {m, d, h, m, s}")
        self.h = h
        self.dttm = datetime(year=YR, month=m, day=d, hour=h, tzinfo=tz)
        print(f"\tD: {self.dttm = }")
        self.dnr = dnr
        self.et = kh0.et(dnr)
        self.DEC = kh.dec(dnr)
        self.LAT = getRandLAT()
        # self.LON = LON if LON else getRandLON()  # qfix
        self.LON = LON


def main():
    print(f"{kh = }, {kh0 = }")


if __name__ == '__main__':
    unittest.main(verbosity=2)
    # main()
