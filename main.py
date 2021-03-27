import minecraft
import maths
import numpy as np

USE_BATCHING = True


def setBlock(block, pos):
    x, y, z = pos
    if USE_BATCHING:
        minecraft.placeBlockBatched(x, y, z, block, 100)
    else:
        minecraft.setBlock(x, y, z, block)


def getBlock(pos):
    x, y, z = pos
    minecraft.getBlock(x, y, z)


def fillBlock(block, pos):
    print(minecraft.runCommand(f"fill %i %i %i %i %i %i {block}" % tuple(pos)))


def setLine(block, pos1, pos2, pixelPerfect=True):
    points = maths.line(pos1, pos2, pixelPerfect)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))


# points = np.array([[272, 71, -210],[266, 100, -235],[296, 87, -267],[328, 76, -283]])
# print(maths.smoothCurveSurface(points))

# setLine("cobblestone", (272, 71, -210), (266, 100, -235))
