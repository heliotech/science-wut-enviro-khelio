============
New `khelio`
============

New version of the `khelio` library
===================================

1. Initializing git repo in local folder (ST-- git: init).
2. Creating remote repo on github (heliotech/science/wut/enviro/khelio):
    git remote add origin https://github.com/heliotech/science-wut-enviro-khelio.git
    git branch -M main
    git push -u origin main
3. Connecting local repo to the remote, git: remote... (and some default options were choisen)
4. Pushing the repo in initial state

Push on 2023.02.12@21:10
------------------------

Untracked files:
    test/get_altitude_fastTest.py
    test/pysolarPlot.py
        Comparison of solar.get_azimuth_fast vs. kh.azi -- excellent results.
    test/pysolarPlot.vym
    test/test_unit.py
        Several tests of kh functions agains pysolar.solar.
    test/test_unit_et.py

Changes:
    Modified   khelio.py
        Some new functions in khelio.py.
    Modified   khelio.rst
    Modified   newkhelio.sublime-workspace

