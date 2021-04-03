from PIL import Image
from worldLoader import WorldSlice
import numpy as np
import requests


def heightmap(xzStart, xzDistance):
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

    for x in range(0, xzDistance[0]):
        for z in range(0, xzDistance[1]):
            biome = slice.getBiomeAt((xzStart[0] + x, 0, xzStart[1] + z))
            y = heightmapData[x][z]
            heightmap.putpixel((x, z), (biome, y, biome))
    heightmap.save("heightmap.png")


# heightmap((0, 0), (512, 512))


def areaCoordinates(xyz1, xyz2):
    # Works for xyz or xz.
    xzStart = (min(xyz1[0], xyz2[0]), min(xyz1[-1], xyz2[-1]))
    xzDistance = (
        (abs(xyz1[0] - xyz2[0])),
        (abs(xyz1[-1] - xyz2[-1])),
    )
    return xzStart, xzDistance


area = areaCoordinates((-256, -256), (256, 256))
heightmap(area[0], area[1])
