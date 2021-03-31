import threading, queue
import main
import requests
from math import sqrt


def surface(xyz):
    """
    Get the surface position of a given xyz coordinates.

    Args:
        xyz (tuple): Coordinates. xyz[1] (Y) matter.

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


q = queue.Queue()
import random


def multiThreadsSurface():  # TODO : Problem with http number of request. See nbt for better solution.
    while True:
        x = q.get()
        for i in range(5):
            print(surface((x, 255, i)))
        q.task_done()


# send thirty task requests to the worker
for x in range(100):
    arg = random.randint(0, 5)
    q.put(x)
    threading.Thread(target=multiThreadsSurface, daemon=True).start()

q.join()


def getChunks(x, z, dx, dz, rtype="text"):  # TODO HERE GET BIOME
    """**Get raw chunk data.**"""
    print(f"getting chunks {x} {z} {dx} {dz} ")

    url = f"http://localhost:9000/chunks?x={x}&z={z}&dx={dx}&dz={dz}"
    print(f"request url: {url}")
    acceptType = "application/octet-stream" if rtype == "bytes" else "text/raw"
    response = requests.get(url, headers={"Accept": acceptType})
    print(f"result: {response.status_code}")
    if response.status_code >= 400:
        print(f"error: {response.text}")

    if rtype == "text":
        return response.text
    elif rtype == "bytes":
        return response.content


# print(type(getChunks(0, 0, 1, 1)))
