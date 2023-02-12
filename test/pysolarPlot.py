# pysolarPlot.py

import datetime
from pysolar import solar
import matplotlib.pyplot as plt
import numpy as np
import pytz

from khelio import ast1, azi, dec, et2
from science.wut.enviro.khelio import hra


def getHra(dt):
    """ 'Extracting' HRA from datetime obj. """

    hr, mn, sc = dt.hour, dt.minute, dt.second
    hrFloat = hr + mn/60 + sc/3600
    result = hra(hrFloat)

    return result


def getDnr(dt):
    return int(dt.strftime("%-j"))


def getAst(dt, LON, LONStd):
    """ Getting AST from a datetime obj. """

    # LON = -LON
    # LONStd = -LONStd
    hr, mn, sc = dt.hour, dt.minute, dt.second
    hrFloat = hr + mn/60 + sc/3600
    dhr = -.4  # seems perfect!
    # dhr = -.45
    hrFloat = hrFloat + dhr
    dnr = getDnr(dt)
    AST = ast1(hrFloat, dnr, LON, LONStd, et2)
    print(f"\tgetAst({dt}, {LON}, {LONStd}) => {AST}")

    return AST


fig, (ax0, ax1) = plt.subplots(2, 1)

td1 = datetime.timedelta(hours=1)
tzWrs = pytz.timezone('Europe/Warsaw')

LAT = 52
LON = 21
LONStd = 15

span = 25  # hours
dts = 1*60*60
dtdl = datetime.timedelta(seconds=dts)
# [base - datetime.timedelta(days=x) for x in range(numdays)]
dtimeRange = np.array([datetime.datetime(2023, 2, 11, tzinfo=tzWrs) +
                       dtdl*i for i in range(span)])
# HRAs = [getHra(dt) for dt in dtimeRange]
ASTs = [getAst(dt, LON, LONStd) for dt in dtimeRange]
HRAs = [hra(AST) for AST in ASTs]
DEC = dec(getDnr(dtimeRange[0]))
khAZI = azi(DEC, LAT, HRAs)

# get_azimuth_fast(latitude_deg, longitude_deg, when):
solAZI = solar.get_azimuth_fast(LAT, LON, dtimeRange)
print(f"{solAZI = }")
print(f"{HRAs = }")
print(f"{ASTs = }")

ax0.plot(dtimeRange, solAZI, label='solAZI')
ax0.plot(dtimeRange, khAZI, label='khAZI')
ax0.legend()
# ax0.scatter(dtimeRange, solAZI)
# ax1.plot(HRAs, label='HRAs')
ax1.plot(ASTs, label='ASTs')

ax0.grid(True)
ax1.grid(True)
plt.legend()
plt.show()
