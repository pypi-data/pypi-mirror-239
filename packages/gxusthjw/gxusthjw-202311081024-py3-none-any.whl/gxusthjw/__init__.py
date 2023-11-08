#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: pygxusthjw包的__init__.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/11/08     revise
# ----------------------------------------------------------------
# 导包 ============================================================
import axs
import commons
import findpeaks
import fityk
import fityk_helpers
import fsd
import ftir
import ma
import mathematics
import matlab
import nmr
import origin_helpers
import peakfit_helpers
import spectrum
import ta
import units
import xrd
import zhxyao

# 定义 ============================================================
__version__ = "0.0.1"

__doc__ = """
the python libraries of gxusthjw.
"""

# noinspection DuplicatedCode
__all__ = [
    'axs',
    'commons',
    'findpeaks',
    'fityk',
    'fityk_helpers',
    'fsd',
    'ftir',
    'ma',
    'mathematics',
    'matlab',
    'nmr',
    'origin_helpers',
    'peakfit_helpers',
    'spectrum',
    'ta',
    'units',
    'xrd',
    'zhxyao',
]
