# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 17:27:16 2014

@author: Alnour_
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1);
y = np.sin(x)
print y
plt.plot(x, y)
