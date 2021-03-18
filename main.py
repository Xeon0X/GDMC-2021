def setBlock(block, pos):
    print("setBolck", pos, block)
    x, y, z = pos
    if USE_BATCHING:
        interfaceUtils.placeBlockBatched(x, y, z, block, 100)
    else:
        interfaceUtils.setBlock(x, y, z, block)


def getBlock(pos):
    x, y, z = pos
    interfaceUtils.setBlock(x, y, z)


def fillBlock(block, pos):
    print(runCommand(f"fill %i %i %i %i %i %i {block}" % tuple(pos)))


def setLine(block, pos1, pos2, pixelPerfect=True):
    points = mathLine(pos1, pos2, pixelPerfect)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))