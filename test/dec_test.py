#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# dec_test.py

from pvlib import solarposition as psp

import numpy as np
import random
from typing import Callable
from pprint import pprint
# import argparse

import sys
sys.path.append("..")

from minihelio import dec

# argParser = argparse.ArgumentParser()
# argParser.add_argument('nrOfDays',
#                        action='store',
#                        nargs='?',  # '*'  # '+'  # argparse.REMAINDER
#                        default='0')
                       
# args = argParser.parse_args()
# try:
#     nrOfDays = int(args.nrOfDays)
# except ValueError:
#     nrOfDays = None
# if nrOfDays is None or nrOfDays < 1:
#     nrOfDays = 10

pvDecs = [psp.declination_spencer71, psp.declination_cooper69]



def checkDecs(fun: Callable, nrDays: int=10, days: list=None) -> dict:
    """Checking solar declination function `fun` against
       functions from pvlib package

       Example:
           >>> results = checkDecs(dec, nrDays=60)
           >>> days = results['days']
           >>> nestedDiffs = list(results['data'][day]['diffs'] for day in days)
           >>> diffs = [item for sublist in nestedDiffs for item in sublist]
           >>> all([diff < 0.40 for diff in diffs])
           True

       Args:
           fun: declination function to be tested.
           nrDays: number of days for the test, optional.
           days: list of days for the test, optional,
                   if present, takes precedence.

       Returns:
           dict: A dictionary with the results, differences and calculated
                   values."""

    if days is not None:
        nrDays = len(days)
    elif nrDays > 0:
        # days = random.sample(range(1, 367), nrDays)
        days = np.random.randint(1, 367, nrDays)

    infoDc = dict([("of", fun.__name__),
                   ("against", [f.__name__ for f in pvDecs])])
    resultDc = dict([("info", infoDc), ("days", days), ("data", dict())])

    for day in days:
        daysDiffs = []
        DEC0 = dec(day)
        dayValues = [DEC0]
        # print(f"D: {day = }, {DEC0 = :.5f}")
        # print("\t", end="")
        for ver_dec in pvDecs:
            DEC1 = np.degrees(ver_dec(day))
            dayValues.append(DEC1)
            diff = (abs(DEC0 - DEC1)/DEC0)
            # print(f"{DEC1 = :.5f}, {diff = :.3f} | ", end="")
            daysDiffs.append(diff)
        resultDc['data'][day] = {'diffs': daysDiffs, 'values': dayValues}
        # print()

    return resultDc


def printCheckresults(results):
    """Printing the results of `checkDecs` (visulalization of the results)"""

    print(f"Comparison of calculations with function `{results['info']['of']}` "
          "against values calculated with "
          f"{str([f for f in results['info']['against']])} from `pvlib`")
    print("="*80)
    diffLen = 12
    header = (f"|{'dnr':^5}|{'Δ1':^{diffLen}}|{'Δ2':^{diffLen}}|"
              f"{'DEC0':^{diffLen}}|{'DEC11':^{diffLen}}|{'DEC12':^{diffLen}}|")
    print(header)
    print("-"*len(header.expandtabs()))
    data = results['data']
    for key in data.keys():
        print(f"|{key:^5}|{data[key]['diffs'][0]:^ {diffLen}.5f}|"
              f"{data[key]['diffs'][1]:^ {diffLen}.5f}|"
              f"{data[key]['values'][0]:^ {diffLen}.5f}|"
              f"{data[key]['values'][1]:^ {diffLen}.5f}|"
              f"{data[key]['values'][2]:^ {diffLen}.5f}|")
    


def main():
    results = checkDecs(dec, 10)  # , days=[3, 57, 98])
    printCheckresults(results)

    print("---------\nresults = ")
    #pprint(results)
    #print(f"{results['data'][57]['diffs'] = }")
    #print(f"{results['data'][57]['values'] = }")
    #print(f"{results['data'][57]['values'][1] = }")
    #print(f"{results['data'][57]['diffs'] = }")
    #for day in results['days']:
    #    print(f"{day = } -> {results['data'][day]['diffs'] = }")
    
    days = results['days']
    nestedDiffs = list(results['data'][day]['diffs'] for day in days)
    diffs = [item for sublist in nestedDiffs for item in sublist]
    for i, diff in enumerate(diffs):
        if abs(diff) > 0.05:
            print(f"{i:>2}) {diff:> 7.5f}")


if __name__ == "__main__":
    main()
