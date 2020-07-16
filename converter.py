#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:09:45 2020

@author: mcgaritym
"""

from IPython.nbformat import v3, v4

with open("capital_bikeshare.py") as fpin:
    text = fpin.read()

nbook = v3.reads_py(text)
nbook = v4.upgrade(nbook)  # Upgrade v3 to v4

jsonform = v4.writes(nbook) + "\n"
with open("capital_bikeshare.ipynb", "w") as fpout:
    fpout.write(jsonform)