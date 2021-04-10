import numpy as np
import random
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import main
import maths
from PIL import Image


def voronoiRandom(
    number, xMinArea, xMaxArea, yMinArea, yMaxArea, y, block, distanceMin
):  # TODO: Delete. Old voronoi.
    """
    Draws a Voronoi diagram in the given points on the specified area.

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


def DELETEvoronoi(
    coordsBuildable,
    coordsNotBuildable,
    xMinArea,
    xMaxArea,
    yMinArea,
    yMaxArea,
    block,
):  # TODO: Delete
    """
    Draws a Voronoi diagram of the given points on the specified area.

    TODO: Refactoring
    """

    coords = coordsBuildable + coordsNotBuildable
    points = np.array((coords))
    vor = Voronoi(points)

    vertices = list(vor.vertices)
    allRegions = list(vor.regions)
    allPointRegions = list(vor.point_region)
    print(allRegions, len(allRegions))
    print(allPointRegions, len(allPointRegions))

    regions = []
    pointRegions = []
    coords = []
    nRegion = -1
    for region in allRegions:
        if -1 not in region:
            nRegion += 1
            if all(
                (xMinArea <= vertices[vertice][0] <= xMaxArea)
                and (yMinArea <= vertices[vertice][1] <= yMaxArea)
                for vertice in region
            ):
                regions.append(region)
                pointRegions.append(allPointRegions[nRegion])

    print(pointRegions, len(pointRegions))
    print(coordsNotBuildable, len(coordsNotBuildable))
    print(coordsBuildable, len(coordsBuildable))
    print(coords, len(coords))
    print(len(regions))

    for i in range(len(regions)):
        if -1 not in regions[i]:
            for j in range(len(regions[i]) - 1):
                print(i, len(pointRegions), len(coords), pointRegions[i])
                if coords[pointRegions[i]] in coordsNotBuildable:
                    mat = "red_concrete"
                else:
                    mat = block
                main.setLine(
                    mat,
                    (
                        vertices[regions[i][j]][0],
                        findGround(
                            (xMinArea, yMinArea),
                            (
                                vertices[regions[i][j]][0],
                                vertices[regions[i][j]][1],
                            ),
                        )[-1],
                        vertices[regions[i][j]][1],
                    ),
                    (
                        vertices[regions[i][j + 1]][0],
                        findGround(
                            (xMinArea, yMinArea),
                            (
                                vertices[regions[i][j + 1]][0],
                                vertices[regions[i][j + 1]][1],
                            ),
                        )[-1],
                        vertices[regions[i][j + 1]][1],
                    ),
                )
                main.setLine(
                    mat,
                    (
                        vertices[regions[i][0]][0],
                        findGround(
                            (xMinArea, yMinArea),
                            (
                                vertices[regions[i][j]][0],
                                vertices[regions[i][j]][1],
                            ),
                        )[-1],
                        vertices[regions[i][0]][1],
                    ),
                    (
                        vertices[regions[i][-1]][0],
                        findGround(
                            (xMinArea, yMinArea),
                            (
                                vertices[regions[i][j + 1]][0],
                                vertices[regions[i][j + 1]][1],
                            ),
                        )[-1],
                        vertices[regions[i][-1]][1],
                    ),
                )


def findGround(xzStart, xz):
    """
    Find the surface at xz using heightmap.

    Args:
        xzStart (tuple): Starting coordinates of the heightmap (northwest corner).
        xz (tuple): Coordinates xz in the Minecraft world.

    Returns:
        tuple: Coordinates xyz in the Minecraft world.
    """
    im = Image.open("heightmap.png")
    x = round(xz[0] - xzStart[0])
    z = round(xz[-1] - xzStart[-1])
    # Alpha is defined as the height ([3]).
    return xz[0], im.getpixel((x, z))[3], xz[-1]


def voronoi(blocks, area, zonesDistrictsPos, xzStart):  # TODO: Refactoring.
    # Coordinates of each district point.
    districtsPos = [
        districtPos for zone in zonesDistrictsPos for districtPos in zone
    ]
    # print(districtsPos, "districtsPos")
    vor = Voronoi(np.array(districtsPos))

    # List of coordinates of each edge.
    edgesPos = vor.vertices
    # List of list of indexes of edges. Each list is a district.
    districtsEdgesInd = vor.regions
    # Actual index = actual coordinates in districtsPos, value = index of the region.
    districtsPointInd = vor.point_region

    # print(edgesPos)
    # print(districtsEdgesInd)
    # print(districtsPointInd)

    districtInd = -1
    for districtPointInd in districtsPointInd:
        districtInd += 1

        # Take districts which are inside the area.
        if -1 not in districtsEdgesInd[districtPointInd]:
            print("a")
            if all(
                (
                    area[0][0] + 1
                    <= edgesPos[districtEdgesInd][0]
                    <= area[1][0] - 1
                )
                and (
                    area[0][1] + 1
                    <= edgesPos[districtEdgesInd][1]
                    <= area[1][1] - 1
                )
                for districtEdgesInd in districtsEdgesInd[districtPointInd]
            ):
                print("b")

                # Find out which area the district belongs to.
                for zone in range(len(zonesDistrictsPos)):
                    if districtsPos[districtInd] in zonesDistrictsPos[zone]:

                        # Place line.
                        for i in range(
                            len(districtsEdgesInd[districtPointInd]) - 2
                        ):
                            main.setLine(
                                blocks[zone],
                                findGround(
                                    xzStart,
                                    edgesPos[
                                        districtsEdgesInd[districtPointInd][i]
                                    ],
                                ),
                                findGround(
                                    xzStart,
                                    edgesPos[
                                        districtsEdgesInd[districtPointInd][
                                            i + 1
                                        ]
                                    ],
                                ),
                            )
                        main.setLine(
                            blocks[zone],
                            findGround(
                                xzStart,
                                edgesPos[
                                    districtsEdgesInd[districtPointInd][0]
                                ],
                            ),
                            findGround(
                                xzStart,
                                edgesPos[
                                    districtsEdgesInd[districtPointInd][-1]
                                ],
                            ),
                        )
