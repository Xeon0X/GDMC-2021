import threading, queue
import main


def surface(xyz):
    """
    Get the surface position of a given xyz coordinates.

    Args:
        xyz (tuple): Coordinates. xyz[2] (Y) matter.

    Returns:
        tuple: Surface coordinates.
    """
    ground = None
    airBlocks = ["minecraft:air", "minecraft:void_air", "minecraft:cave_air"]

    if (
        main.getBlock((xyz[0], xyz[1], xyz[2])) in airBlocks
    ):  # Position is air.
        while ground == None:
            if (
                main.getBlock((xyz[0], xyz[1], xyz[2])) in airBlocks
            ):  # Position is air.
                xyz = xyz[0], xyz[1] - 1, xyz[2]
            else:
                ground = xyz

    elif (
        main.getBlock((xyz[0], xyz[1] + 1, xyz[2])) in airBlocks
    ):  # Position is the surface.
        ground = (xyz[0], xyz[1], xyz[2])

    else:  # Position is under the surface.
        while ground == None:
            if (
                main.getBlock((xyz[0], xyz[1] + 1, xyz[2])) in airBlocks
            ):  # Position is air, surface found.
                ground = (xyz[0], xyz[1] - 1, xyz[2])
            else:
                xyz = (xyz[0], xyz[1] + 1, xyz[2])

    return xyz