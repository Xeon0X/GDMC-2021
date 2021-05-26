import main
import maths

import random
import numpy as np
from PIL import Image
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import roads

print("map.py")


def DELETEvoronoiRandom(
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


def DELETEvoronoiCurve(
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
    xs, ys, zs = maths.curve(
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


def findGround(xzStart, xz):  # TODO: Change error.
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
    width, height = im.size
    if x >= width or z >= height:
        print("img:", x, z)
        print(width, height)
        print(xzStart, xz)
    try:
        return xz[0], im.getpixel((x, z))[2], xz[-1]
    except:
        print("Error getpixel in map.py:309 with ", x, z)
        return None


def DELETEvoronoi(
    blocks, area, zonesDistrictsPos, xzStart
):  # TODO: Refactoring.
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


def voronoi2(
    blocks, area, zonesDistrictsPos, xzStart
):  # TODO: Refactoring but not with voronoi.
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

    print(edgesPos)
    print(districtsEdgesInd)
    print(districtsPointInd)
    print(districtsPos)

    districtInd = -1
    for districtPointInd in districtsPointInd:
        districtInd += 1

        # Take districts which are inside the area.
        if -1 not in districtsEdgesInd[districtPointInd]:
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

                # raod.intersection(
                #     standard_modern_lanes_agencement,
                #     (20, 250, 120),
                #     {
                #         0: ((20, 250, 200), (-20, 250, 60)),
                #         1: ((60, 250, 60), (-50, 250, 150)),
                #     },
                #     {0: (-100, 250, 100), 1: (100, 250, 100)},
                # )
                # Find out which area the district belongs to.
                for zone in range(len(zonesDistrictsPos)):
                    if districtsPos[districtInd] in zonesDistrictsPos[zone]:

                        # Place line.
                        for i in range(
                            len(districtsEdgesInd[districtPointInd])
                        ):
                            intersection_center = []
                            intersection = []
                            for j in range(len(districtsEdgesInd)):
                                if j != districtPointInd:
                                    for k in range(len(districtsEdgesInd[j])):
                                        if (
                                            districtsEdgesInd[
                                                districtPointInd
                                            ][i]
                                            == districtsEdgesInd[j][k - 1]
                                        ):
                                            # print(
                                            #     districtsEdgesInd[
                                            #         districtPointInd
                                            #     ][i],
                                            #     districtsEdgesInd[j],
                                            #     districtsEdgesInd[j][k],
                                            #     districtsEdgesInd[j][k - 1],
                                            #     districtsEdgesInd[j][k - 2],
                                            # )
                                            if (
                                                districtsEdgesInd[
                                                    districtPointInd
                                                ][i]
                                                not in intersection_center
                                            ):
                                                intersection_center.append(
                                                    districtsEdgesInd[
                                                        districtPointInd
                                                    ][i]
                                                )
                                            if (
                                                districtsEdgesInd[j][k]
                                                not in intersection
                                            ):
                                                intersection.append(
                                                    districtsEdgesInd[j][k]
                                                )
                                            if (
                                                districtsEdgesInd[j][k - 2]
                                                not in intersection
                                            ):
                                                intersection.append(
                                                    districtsEdgesInd[j][k - 2]
                                                )
                            # print(intersection_center, intersection)
                            if -1 not in intersection:
                                # image index out of range
                                g2 = findGround(
                                    xzStart,
                                    list(edgesPos[intersection[-2]]),
                                )
                                g1 = findGround(
                                    xzStart,
                                    list(edgesPos[intersection[-1]]),
                                )
                                g0 = findGround(
                                    xzStart,
                                    list(edgesPos[intersection_center[0]]),
                                )
                                print("G0", g0, g1, g2)

                                if g0 != None and g1 != None and g2 != None:
                                    print("G", g0, g1, g2)
                                    pointDico = {}
                                    mainDico = (
                                        g2,
                                        g1,
                                    )
                                    for a in range(0, len(intersection) - 2):
                                        if (
                                            findGround(
                                                xzStart,
                                                list(
                                                    edgesPos[intersection[a]]
                                                ),
                                            )
                                            != None
                                        ):
                                            pointDico[a] = findGround(
                                                xzStart,
                                                list(
                                                    edgesPos[intersection[a]]
                                                ),
                                            )
                                        else:
                                            print("Error here")

                                    print("g0: ", g0)
                                    print("mainDico: ", mainDico)
                                    print("pointDico: ", pointDico)
                                    if pointDico != {}:
                                        roads.intersection(
                                            roads.standard_modern_lanes_agencement,
                                            g0,
                                            {0: mainDico},
                                            pointDico,
                                        )
                                    print("build")
                                else:
                                    print("it's ok")
