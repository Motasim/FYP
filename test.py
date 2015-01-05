# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 19:48:16 2014

@author: Alnour_
"""
class point:
    def __init__(self , x , y):
        self._x = x
        self._y = y
import numpy as np
def sqr_dist(p1 , p2):
    return (p1._x-p2._x)**2 + (p1._y-p2._y)**2
def angle(p2 , p1 , p3): #p1 is the center
    p12 = sqr_dist(p1,p2)
    p13 = sqr_dist(p1,p3)
    p23 = sqr_dist(p2,p3)
    N = p12+p13-p23 *1.0
    D = 2* np.sqrt(p12) * np.sqrt(p13)
    return np.arccos(N/D)