import interfaceUtils as minecraft
import numpy as np
from worldLoader import WorldSlice
import maths

USE_BATCHING = True


def setBlock(block, xyz):
    x, y, z = xyz
    if USE_BATCHING:
        minecraft.placeBlockBatched(x, y, z, block, 100)
    else:
        minecraft.setBlock(x, y, z, block)


def getBlock(xyz):
    x, y, z = xyz
    return minecraft.getBlock(x, y, z)


def fillBlock(block, xyz):
    print(minecraft.runCommand(f"fill %i %i %i %i %i %i {block}" % tuple(xyz)))


def setLine(block, xyz0, xyz1, pixelPerfect=True):
    points = maths.line(xyz0, xyz1, pixelPerfect)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))


def setCurveSurface(block, points, distance):  # HERE
    """
    Create a curve with a thickness inside Minecraft.

    Args:
        block (str): Minecraft block.
        points (numpy.ndarray): Points where the curve should go.
        distance (int): Thickness.

    >>> setCurveSurface(
            "minecraft:stone",
            np.array(
                [
                    [-19, 71 + 25, -174],
                    [-3, 75 + 15, -291],
                    [8, 79 + 25, -279],
                    [12, 69 + 15, -270],
                    [0, 63 + 25, -248],
                ]
            ),
            5,
        )

    TODO:
        Fix USE_BATCHING = True : end blocks are not correct.
        Finish the function.

    """
    curve = maths.curveSurface(points, distance, resolution=0)
    for lane in curve:
        for xyz in curve[lane]:
            setBlock("stone", xyz)
    for lane in curve:
        c = 0
        for xyz in curve[lane]:
            c += 1
            if lane == 0:
                if c % 3 != 0:
                    setBlock("white_concrete", xyz)
            if lane == 8:
                setBlock("white_concrete", (xyz[0], xyz[1], xyz[2]))
            if lane == -8:
                setBlock("yellow_concrete", xyz)
            if lane == -7:
                setBlock("red_concrete", xyz)
            if lane == -6:
                setBlock("yellow_concrete", xyz)
            if lane == -10:
                setBlock("red_concrete", xyz)