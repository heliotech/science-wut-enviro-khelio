# minihelio.py

"""minihelio engineering library

Basic functions and methods for solar engineering with Python

Variables:
----------
`mtDays`: dictionary with the sum of days
        in the previous month(s) (if any)

Functions:
----------
`dayNr(*args)`: calculates the number of a day in the year,
              for different arguments
              
`dec(dn)`: calculates solar declination for the given day.

------------------------------------------------------------------------

"""

import numpy as np


d2r = np.float64(np.pi/180)  # degrees to radians

mtDays = {1: 0, 2: 31, 3: 59,
          4: 90, 5: 120, 6: 151,
          7: 181, 8: 212, 9: 243,
          10: 273, 11: 304, 12: 334}
"""mtDays: a dictionary with numbers of days 
             up to certain month (included)"""


def _oneDayNr(m, d):
    """'Internal' method, returns number of the day in a year
    for a single day and common year.
    """

    return d + mtDays[m]


def dayNr(*args):
    """Number of the day in a year dayNr = f(mm, dd): month, day
    or f((mm, dd)).

    Examples:
        >>> from datetime import datetime
        >>> dayNr(3, 21) == datetime(2022, 3, 21).timetuple().tm_yday
        True
        >>> dayNr(6, 22) == datetime(2022, 6, 22).timetuple().tm_yday
        True

    Args:
        m (int): A number of the month.
        d (int): A number of the day.
        or (m, d): a tuple of the numbers.

    Returns:
        int: A number of the day in year.

    Raises:
        ValueError: An error for invalid date.

    ! datetime.strftime("%-j") -- the same!
    """

    if (len(args) == 2):
        mm = args[0]
        dd = args[1]
    elif len(args) == 1 and isinstance(args[0], tuple):
        mm = args[0][0]
        dd = args[0][1]
    elif isinstance(args[0], np.ndarray) or isinstance(args[0], list):
        results = np.array([], dtype=int)
        for tp in args[0]:
            results = np.append(results, _oneDayNr(tp[0], tp[1]))
        return results
    else:
        raise TypeError("Wrong date format (should be (m, d)).")
    if mm > 12 or dd > 31:
        raise ValueError("Invalid date")
    return _oneDayNr(mm, dd)


def dec(dn):
    """Solar declination DEC = dec(dn), with domain check.
    
    The input argument, `dn` cannot exceed 366.
    
    Examples:
        >>> import khelio as kh
        >>> diff = abs((dec(1) - kh.decC0(1))/dec(1))
        >>> round(diff, 3) < 0.005
        True
        >>> dec(40) == kh.dec(40)
        True

    Args:
        dn (int): Number of the day in the year
        
    Returns:
        float: Value of the solar declination in given day.

    Raises:
        ValueError: For day number greater than 366.
    """

    if dn > 366:
        raise ValueError("Day number > 366.")
    return 23.45 * np.sin( (360.0 * (np.array(dn) + 284.0)/365.0)*d2r )


def testDayNr():
    dates = [(3, 21), (6, 22)]
    for i, date in enumerate(dates):
        print(f"{i}) {date = } -> dayNr({date}) = {dayNr(date)}")

def main():
    testDayNr()


if __name__ == "__main__":
    main()
