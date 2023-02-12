# get_altitude_fastTest.py

# from pysolar.solar import get_declination, get_altitude_fast

# import khelio as kh

import datetime
from datetime import timezone
from pysolar import solar
import pytz

import khelio as kh
from misc import foritemin

# def get_altitude_fast(latitude_deg, longitude_deg, when):

# for i, tz in enumerate(pytz.common_timezones):
#     print(f"{i}) {tz = }")

YR = 2023
UTC = datetime.timezone.utc


def getMD(dt):
    """ Gets month, day from datetime """

    m, d = dt.month, dt.day
    return m, d


def getHM(dt, dec=False):
    """ Gets hour, minute from datetime """

    h, m = dt.hour, dt.minute

    if not dec:
        return h, m
    else:
        return h + m/60


td1 = datetime.timedelta(hours=1)
td2 = datetime.timedelta(hours=2)
print(f"{datetime.timezone.utc = }")
print(f"{pytz.timezone('Europe/Warsaw') = }")
print(f"{pytz.timezone('Europe/London') = }")
tzWar = pytz.timezone("Europe/Warsaw")
tz1 = datetime.timezone(td1)
tz2 = datetime.timezone(td2)
foritemin(tzWar)
print(f"{datetime.timezone(td1) = }")
print(f"{datetime.timezone(td2) = }")
print(f"{tz1 = }")
print(f"{UTC.utcoffset(None) = }")  # THAT'S IT!!!
print(f"{tz1.utcoffset(None) = }")
print(f"{tzWar.utcoffset(datetime.datetime.now()) = }")

# def get_solar_time(longitude_deg, when):
dttm = datetime.datetime(YR, 2, 11, 4, 23, tzinfo=tz1)
print(f"{dttm = }")
LAT = 52
LON = 21
LONStd = 15
solSolarT = solar.get_solar_time(LON, dttm)
print(f"{solSolarT = }")
# def ast1(LST, dnr, LON, LONStd):
dnr = kh.dayNr(2, 11)
print(f"{getHM(dttm) = }")
khAST = kh.ast1(getHM(dttm, dec=True), dnr, LON, LONStd)
tDiff = abs(solSolarT - khAST)
print(f"{khAST = }, {tDiff = :.5f} [h] = {tDiff*60:.5f} [min] = "
      f"{tDiff*3600:.5f} [sec]")

solALT = solar.get_altitude_fast(LAT, LON, dttm)
print(f"{solALT = }")
DEC = kh.dec(kh.dayNr(getMD(dttm)))
HRA = kh.hra(khAST)
khALT = kh.alt(DEC, LAT, HRA)
diffALT = abs(solALT - khALT)
print(f"{khALT = }, {diffALT = :.5f}")

# def get_azimuth_fast(latitude_deg, longitude_deg, when):
solAZI = solar.get_azimuth_fast(LAT, LON, dttm)
khAZI = kh.azi(DEC, LAT, HRA)
diffAZI = abs(solAZI - khAZI)
print(f"{solAZI = }")
print(f"{khAZI = }, {diffAZI = :.5f}")

dttm328 = datetime.datetime(YR, 3, 28, 16, 45, tzinfo=tz2)
solAZI328 = solar.get_azimuth_fast(LAT, LON, dttm328)
khAST1645 = kh.ast1(getHM(dttm328, dec=True), dnr, LON, LONStd)
DEC328 = kh.dec(kh.dayNr(getMD(dttm328)))
HRA1645 = kh.hra(khAST1645)
khAZI328 = kh.azi(DEC328, LAT, HRA1645)
diffAZI328 = abs(solAZI328 - khAZI328)
print(f"{solAZI328 = }")
print(f"{khAZI328 = }, {diffAZI328 = :.5f}")
