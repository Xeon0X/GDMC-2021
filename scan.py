from PIL import Image
from worldLoader import WorldSlice
import numpy as np


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
            y = heightmapData[x][z]
            heightmap.putpixel((x, z), (y, y, y))
    heightmap.save("heightmap.png")