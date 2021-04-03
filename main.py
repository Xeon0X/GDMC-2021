import minecraft
import maths
import numpy as np
from worldLoader import WorldSlice

USE_BATCHING = True


def setBlock(block, pos):
    x, y, z = pos
    if USE_BATCHING:
        minecraft.placeBlockBatched(x, y, z, block, 100)
    else:
        minecraft.setBlock(x, y, z, block)


def getBlock(pos):
    x, y, z = pos
    return minecraft.getBlock(x, y, z)


def fillBlock(block, pos):
    print(minecraft.runCommand(f"fill %i %i %i %i %i %i {block}" % tuple(pos)))


def setLine(block, pos1, pos2, pixelPerfect=True):
    points = maths.line(pos1, pos2, pixelPerfect)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))