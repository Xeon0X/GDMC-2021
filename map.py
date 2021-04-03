import numpy as np
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import main
import maths


def voronoi(
    number, xMinArea, xMaxArea, yMinArea, yMaxArea, y, block, distanceMin
):  # HERE
    """
    Draws a Voronoi diagram of the given points on the specified area.

    Args:
        number (int): number of random points
        xMinArea (int): [description]
        xMaxArea ([type]): [description]
        yMinArea ([type]): [description]
        yMaxArea ([type]): [description]
        y ([type]): [description]
        block ([type]): [description]
        distanceMin ([type]): [description]

    TODO: Delete random points because we have now a heightmap.
    TODO: Refactoring
    """
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
    print(vor.vertices)
    print(vor.regions)

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

    fig = voronoi_plot_2d(vor)
    plt.show()


def voronoiCurve(
    number, xMinArea, xMaxArea, yMinArea, yMaxArea, y, block, distanceMin
):  # TODO: Delete, just for fun.
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

    ppoints1 = []
    ppoints2 = []
    ppoints3 = []
    for i in range(len(regions)):
        if -1 not in regions[i]:
            for j in range(1, len(regions[i]) - 2):
                ppoints1.append(
                    (
                        vertices[regions[i][j]][0],
                        random.randint(56, 60),
                        vertices[regions[i][j]][1],
                    )
                )
                ppoints2.append(
                    (
                        vertices[regions[i][j]][0] + random.randint(-5, 5),
                        random.randint(56, 60),
                        vertices[regions[i][j]][1] + random.randint(-5, 5),
                    )
                )
                ppoints3.append(
                    (
                        vertices[regions[i][j]][0] + random.randint(-5, 5),
                        random.randint(56, 60),
                        vertices[regions[i][j]][1] + random.randint(-5, 5),
                    )
                )
    ppoints = ppoints1 + ppoints2 + ppoints3
    xs, ys, zs = maths.smoothCurve(
        (ppoints),
        number_true_pts=900,
        debug=False,
    )
    l = 0
    for k in range(len(xs) - 1):
        pos0 = xs[k], ys[k], zs[k]
        pos1 = (xs[k + 1], ys[k + 1], zs[k + 1])
        main.setLine(block[l], pos0, pos1)
        if l < 13:
            l += 1
        else:
            l = 0
