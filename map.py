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
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import main
import maths


def voronoi(
    number, xMinArea, xMaxArea, yMinArea, yMaxArea, y, block, distanceMin
):
    randomCoords = []
    for i in range(0, number):
        randomCoords.append(
            [
                random.randint(xMinArea, xMaxArea),
                random.randint(yMinArea, yMaxArea),
            ]
        )

    coords = []
    for randomCoord in randomCoords:
        if all(
            maths.distance2D(randomCoord, coord) > distanceMin
            for coord in coords
        ):
            coords.append(randomCoord)

    points = np.array(coords)
    vor = Voronoi(points)

    vertices = list(vor.vertices)
    allRegions = list(vor.regions)

    regions = []
    for region in allRegions:
        if -1 not in region:
            if all(
                (xMinArea <= vertices[vertice][0] <= xMaxArea)
                and (yMinArea <= vertices[vertice][1] <= yMaxArea)
                for vertice in region
            ):
                regions.append(region)

    for i in range(len(regions)):
        if -1 not in regions[i]:
            for j in range(len(regions[i]) - 1):
                main.setLine(
                    block,
                    (
                        vertices[regions[i][j]][0],
                        y,
                        vertices[regions[i][j]][1],
                    ),
                    (
                        vertices[regions[i][j + 1]][0],
                        y,
                        vertices[regions[i][j + 1]][1],
                    ),
                )
                main.setLine(
                    block,
                    (
                        vertices[regions[i][0]][0],
                        y,
                        vertices[regions[i][0]][1],
                    ),
                    (
                        vertices[regions[i][-1]][0],
                        y,
                        vertices[regions[i][-1]][1],
                    ),
                )

    # fig = voronoi_plot_2d(vor)
    # plt.show()


print("test 0")
voronoi(100, -512, 512, -512, 512, 56, "stone", 100)
print("test")