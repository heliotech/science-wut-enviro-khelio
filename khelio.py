# -*- coding: utf-8 -*-
"""
=======================================================================
                     Solar engineering library
=======================================================================
author: Sebastian M. Kazimierski
date: 2023.02.09
"""

from math import modf
import numpy as np
from numpy import sin, cos, pi

fname = __file__.split('/')[-1].split('.')[0]

""" Constants """

d2r = np.float64(pi/180)
r2d = np.float64(180/pi)

mtDaysSum = {1: 0, 2: 31, 3: 59,
             4: 90, 5: 120, 6: 151,
             7: 181, 8: 212, 9: 243,
             10: 273, 11: 304, 12: 334}

# Recommended days: dates
rMDays = [(1, 17), (2, 16), (3, 16), (4, 15), (5, 15), (6, 11),
          (7, 17), (8, 16), (9, 15), (10, 15), (11, 14), (12, 10)]

days7 = [(1, 21), (2, 20), (3, 20), (4, 20), (5, 21), (6, 21), (12, 21)]
days3 = [(3, 22), (6, 21), (12, 21)]


def oneDayNr(m, d):
    """'Internal' method, returns number of the day in a year
    for a single day and common year.
    """

    return d + mtDaysSum[m]


def dayNr(*args):
    """Compute number of the day in a common year.

    Args:
        m (int): number of the month.
        d (int): number of the day.
        Or
        (m, d) (tuple(int, int)).

    Returns:
        int - the number of a day in the year.

    Ref.
        Pluta 2006
    """
    try:
        mm, dd = args
    except ValueError:
        results = np.zeros(len(args[0]), dtype=int)
        for i, date in enumerate(args[0]):
            dnr = dayNr(*date)
            results[i] = dnr
        return results

    return oneDayNr(mm, dd)


def dec(dn):
    """Solar declination DEC = dec(dn) (degrees).

    Args:
        dn (int) - number of the day in a year.

    Returns:
        float - value of the solar declination angle.
    """

    if not isinstance(dn, np.ndarray):
        dn = np.array(dn)
    return 23.45 * sin((360.0 * (dn + 284.0)/365.0)*d2r)


# hour angle, HRA, 15*(tau-12.00) [degrees]
def hra(h):
    """The hour angle function,
    !TODO: docstring
    HRA = hra(tau): HRA - the hour angle, tau - the hour."""
    if (hasattr(h, '__iter__')):
        # return [15*(t - 12.00) for t in tau]
        return [hra(t) for t in h]
    else:
        dt = 0 if h >= 0 else 24
        return 15*((dt + h) - 12.00)  # degrees


def hr(HRA):
    """
    The hour for an hour angle (omega)
    !TODO: docstring
    """
    if hasattr(HRA, "__iter__"):
        return [hr(a) for a in HRA]
    else:
        return (HRA/15) + 12


def timeDec2HMS(time, *args, **kwargs):
    """timeDec2HMS -- time as a decimal number to (h, m, s)
    !TODO: docstring
    Arguments: time -- decimal hour/time; True or String=True for string output;
    prec for precision (string), or prec=0 for integer."""
    if 'string' in kwargs:
        string = kwargs['string']
    else:
        string = False

    sign = np.sign(time)
    if sign == -1:
        signS = '-'
    elif sign == 1:
        signS = ''
    else:
        signS = ''

    SPrec = kwargs['prec'] if 'prec' in kwargs else 0
    if len(args) > 0 and isinstance(args[0], bool):
        string = args[0]
    if len(kwargs) > 0 and 'String' in kwargs:
        string = kwargs['String']
    if len(kwargs) > 0 and 'prec' in kwargs:
        SPrec = kwargs['prec']
    timeF = abs(modf(time)[0])
    minutes = round(abs(timeF*60), 12)
    minutesF = abs(modf(minutes)[0])
    seconds = abs(minutesF*60)
    # if seconds == 60:
    #     seconds = 0
    #     minutes += 1
    if not string:
        if SPrec > 0:
            return (int(time), int(minutes), round(seconds, SPrec))
        else:
            return (int(time), int(minutes), int(seconds))
    else:
        return ('{sign}{H:02}:{M:02}:{S:02.{prec}f}'
                .format(sign=signS, H=int(time), M=int(minutes), S=seconds,
                        prec=SPrec))


def hra_minitest():
    hrs = np.random.rand(10)*24  # 10 random hours
    for i, h in enumerate(hrs):
        print(f"{i}) hra({h}) = {hra(h)}")
    print(f"{hra(hrs) = }")


def zen(DEC, LAT, HRA):
    """Solar zenith angle ZEN = zen(DEC, LAT, HRA) (degrees)

    Args:
        DEC (float) - solar declination angle.
        LAT (float) - geographical latitude of location.
        HRA (float) - hour angle.

    Returns:
        float - solar zenith angle.
    """
    return np.arccos(np.cos(LAT*d2r)*np.cos(DEC*d2r)*np.cos(HRA*d2r) +
                     np.sin(LAT*d2r)*np.sin(DEC*d2r))/d2r


def alt(DEC, LAT, HRA, dtype=np.float32):
    """Solar altitude angle ALT = alt(DEC, LAT, HRA) (degrees)

    Args:
        DEC (float) - solar declination angle.
        LAT (float) - geographical latitude of location.
        HRA (float) - hour angle.
        dtype (type) - type of the return value, default np.float32.

    Returns:
        float - solar azimuth angle.
    """
    DEC = np.asarray(DEC, dtype=dtype)
    LAT = np.asarray(LAT, dtype=dtype)
    HRA = np.asarray(HRA, dtype=dtype)
    return np.arcsin(np.cos(LAT*d2r)*np.cos(DEC*d2r)*np.cos(HRA*d2r)
                     + np.sin(LAT*d2r)*np.sin(DEC*d2r))/d2r


def inc(DEC, LAT, TIL, ORI, HRA):
    """Angle of incidence, INC = inc(DEC, LAT, TIL, ORI, HRA) (degrees)

    Args:
        DEC (float) - solar declination angle.
        LAT (float) - geographical latitude of location.
        TIL (float) - tilt of the surface in question.
        ORI (float) - orientation of the surface, from (-180, 180);
                      if (0, 360) => ORI = ORI - 180
        HRA (float) - hour angle.

    Returns:
        float - solar incidence angle.

    Ref.:
        Chen PSE (4.37)
    """
    cosINC = (sin(DEC*d2r)*(sin(LAT*d2r)*cos(TIL*d2r) -
              cos(LAT*d2r)*sin(TIL*d2r)*cos(ORI*d2r)) +
              cos(DEC*d2r)*(cos(LAT*d2r)*cos(TIL*d2r)*cos(HRA*d2r) +
                            sin(LAT*d2r)*sin(TIL*d2r)*cos(ORI*d2r)*cos(HRA*d2r)
                            + sin(TIL*d2r)*sin(ORI*d2r)*sin(HRA*d2r)))

    return np.arccos(cosINC)*r2d


def main():
    hra_minitest()


if __name__ == '__main__':
    main()
