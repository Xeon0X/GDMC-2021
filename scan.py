from worldLoader import WorldSlice
import numpy as np
import requests
import cv2
import maths
import random
import map
from PIL import Image


def heightmap(xzStart, xzDistance):  # TODO: Can be better and clear.
    """
    Generate a heightmap with nbt data.

    Args:
        xzStart (tuple): xz coordinates of the northwest corner of the
        area to scan.
        xzDistance (tuple): xz distance of the southwest corner from the
        northwest corner.

    Returns:
        heightmap.png

    >>> heightmap((-256, -256), (512, 512))
    """

    heightmap = Image.new(
        "RGB",
        (xzDistance[0], xzDistance[1]),
        "red",
    )

    slice = WorldSlice((xzStart[0], xzStart[1], xzDistance[0], xzDistance[1]))
    heightmapData = list(
        np.array(slice.heightmaps["OCEAN_FLOOR"], dtype=np.uint8)
    )

    waterBlocks = [
        "minecraft:water",
        "minecraft:seagrass",
        "minecraft:tall_seagrass",
        "minecraft:kelp_plant",
    ]
    for x in range(0, xzDistance[0]):
        for z in range(0, xzDistance[1]):
            biome = slice.getBiomeAt((xzStart[0] + x, 0, xzStart[1] + z))
            y = heightmapData[x][z]
            blockAt = slice.getBlockAt((xzStart[0] + x, y, xzStart[1] + z))
            if biome == 1:
                heightmap.putpixel((x, z), (y, 50, y))
            else:
                heightmap.putpixel((x, z), (50, y, y))
    heightmap.save("heightmap.png")


def voronoiCoordinates(
    blocks, area, distanceMin1, distanceMin2
):  # TODO:Better
    xyz1, xyz2 = area
    xzStart, xzDistance = areaCoordinates(xyz1, xyz2)
    heightmap(xzStart, xzDistance)
    im = Image.open("heightmap.png")

    # Creating points depending of  the heightmap.
    buildable = []
    notBuildable = []
    notBuildable2 = []

    for x in range(0, xzDistance[0]):
        for z in range(0, xzDistance[1]):
            __, g, b = im.getpixel((x, z))
            if b >= 80:
                notBuildable2.append((xzStart[0] + x, xzStart[1] + z))
            elif g == 50:
                buildable.append((xzStart[0] + x, xzStart[1] + z))
            else:
                notBuildable.append((xzStart[0] + x, xzStart[1] + z))

    # Sorting points depending of the distance.
    coordsBuildable = []
    coordsNotBuildable = []
    coordsNotBuildable2 = []

    for build in buildable:
        if all(
            maths.distance2D(build, coord) > distanceMin1
            for coord in coordsBuildable
        ):
            coordsBuildable.append(build)

    for notBuild in notBuildable:
        if all(
            maths.distance2D(notBuild, coord) > distanceMin2
            for coord in coordsNotBuildable
        ):
            coordsNotBuildable.append(notBuild)

    for notBuild2 in notBuildable2:
        if all(
            maths.distance2D(notBuild2, coord) > distanceMin2
            for coord in coordsNotBuildable2
        ):
            coordsNotBuildable2.append(notBuild2)

    # Generating voronoi.
    zonesDistrictsPos = (
        [coordsBuildable] + [coordsNotBuildable] + [coordsNotBuildable2]
    )
    areaMinMax = (
        (min(area[0][0], area[1][0]), min(area[0][-1], area[1][-1])),
        (max(area[0][0], area[1][0]), max(area[0][-1], area[1][-1])),
    )
    print(areaMinMax)
    map.voronoi(blocks, areaMinMax, zonesDistrictsPos, xzStart)


def areaCoordinates(xyz1, xyz2):
    """
    Transform an area into a start point and a distance. Work with xyz
    coordinates and xz coordinates.

    Args:
        xyz1 (tuple): Coordinates, whatever the direction.
        xyz2 (tuple): Coordinates, whatever the direction.

    Returns:
        tuple: xzStart, xzDistance
    """
    xzStart = (min(xyz1[0], xyz2[0]), min(xyz1[-1], xyz2[-1]))
    xzDistance = (
        (abs(xyz1[0] - xyz2[0])),
        (abs(xyz1[-1] - xyz2[-1])),
    )
    return xzStart, xzDistance


blocks = [
    "minecraft:white_concrete",
    "minecraft:red_concrete",
    "minecraft:blue_concrete",
]
voronoiCoordinates(blocks, ((15, 294), (-339, -39)), 70, 40)