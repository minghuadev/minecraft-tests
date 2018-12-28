# -*- coding: utf-8 -*-
"""
    local_numpy.py
    ==============
"""

def log2(x):
    if type(x) is not int:
        raise Exception("local_numpy.py log2 x type error")
    b = 1
    for i in range(32):
        y = b << i
        if y == x:
            return i
        if y > x:
            raise Exception("local_numpy.py log2 x value not a power of 2")
    raise Exception("local_numpy.py log2 x value not a power of 2 in 32-bit ramge")
