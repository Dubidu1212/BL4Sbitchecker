#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mockup data visualisation plot for BL4S application.
"""


import matplotlib.pyplot as plt

import numpy as np


# mockup data
labels = ["0.01", "0.1", "1", "10"]
filesize = 1000000 #bit
upswitch = np.array((1, 7, 53, 342)) / filesize * 1000000
downswitch = np.array((1, 5, 46, 310)) / filesize * 1000000
width = 0.6


# plot generation
plt.style.use("ggplot")

fig = plt.figure(figsize=(8,4))
ax = fig.subplots()

ax.bar(labels, upswitch, width, label='bitflip 0 -> 1')
ax.bar(labels, downswitch, width, bottom=upswitch, label='bitflip 1 -> 0')

plt.title("Bit Flips of SSD Drives")
plt.xlabel("accumulated radiation / J")
plt.ylabel("flipped bits / ppm")
plt.legend(loc="upper left")
ax.text(0.5, 0.5, 'mockup data', transform=ax.transAxes,
        fontsize=20, color='gray', alpha=0.5,
        ha='center', va='center')

plt.savefig("result-simulation-1.pdf")
plt.show()