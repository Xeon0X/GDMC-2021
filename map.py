# TODO(@Xeon0X): Procedural highways, main roads, streets, districts and
# blocks generator.
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
# Generate random points inside the area. Maybe make random points using height
# maps.
# Kill points that are too close.
# Generate the graph, take all the edges.
# Cut edges that are outside the area.
# Generate roads with probability on edges.

import numpy as np
import random

a = []
for i in range(100):
    a.append([random.uniform(-5, 5), random.uniform(-5, 5)])

print(a)

points = np.array(a)
from scipy.spatial import Voronoi, voronoi_plot_2d

vor = Voronoi(points)

import matplotlib.pyplot as plt

print(vor.vertices)

fig = voronoi_plot_2d(vor)
plt.show()
