"""
Roads generator for Minecraft 1.16.3 using GDMCHTTP. 
Made for the Generative Design in Minecraft Competition
Author: Xeon0X
Date: 12/22/2020
"""

############################ Initialization ############################

import requests
from math import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D

import time
import random
import interfaceUtils

url = "http://localhost:9000/command"

USE_BATCHING = True

wolrdMaxHeight = 255

############################ Basic Commands ############################


def runCommand(command):
    # time.sleep(0.1)
    print("running cmd %s" % command)
    response = requests.post(url, bytes(command, "utf-8"))
    return response.text


# -----------------------------------------------------------------------


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


# -----------------------------------------------------------------------


def setLine(block, pos1, pos2, pixelPerfect=True):
    points = mathLine(pos1, pos2, pixelPerfect)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))


def setLineRandom(block1, block2, pos1, pos2, pixelPerfect=False):
    points = mathLine(pos1, pos2, pixelPerfect)

    for i in points:
        if random.randint(0, 2) == 0:
            setBlock(block2, (i[0], i[1], i[2]))
        else:
            setBlock(block1, (i[0], i[1], i[2]))


def findGround(pos):
    ground = None

    if (
        runCommand(f"execute unless block %i %i %i air" % tuple(pos))
        == "Test failed"
    ):  # pos is air
        while ground == None:
            if (
                runCommand(f"execute unless block %i %i %i air" % tuple(pos))
                == "Test failed"
            ):  # pos is air
                pos = pos[0], pos[1] - 1, pos[2]
            else:
                ground = pos

    elif (
        runCommand(
            f"execute unless block %i %i %i air" % (pos[0], pos[1] + 1, pos[2])
        )
        == "Test failed"
    ):  # pos is the surface
        ground = (pos[0], pos[1], pos[2])

    else:  # pos is under the surface
        while ground == None:
            if (
                runCommand(f"execute unless block %i %i %i air" % tuple(pos))
                == "Test failed"
            ):  # pos is air, surface find
                ground = (pos[0], pos[1] - 1, pos[2])
            else:
                pos = pos[0], pos[1] + 1, pos[2]

    return pos


# -----------------------------------------------------------------------


def mathLine(pos1, pos2, pixelPerfect=True):
    """
    https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/
    pixelPerfect is not 100% accurate, blocks are missings at the end of the line.
    """
    (x1, y1, z1) = pos1
    (x2, y2, z2) = pos2
    x1, y1, z1, x2, y2, z2 = (
        round(x1),
        round(y1),
        round(z1),
        round(x2),
        round(y2),
        round(z2),
    )

    ListOfPoints = []
    ListOfPoints.append((x1, y1, z1))
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dz = abs(z2 - z1)
    if x2 > x1:
        xs = 1
    else:
        xs = -1
    if y2 > y1:
        ys = 1
    else:
        ys = -1
    if z2 > z1:
        zs = 1
    else:
        zs = -1

    # Driving axis is X-axis
    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != x2:
            x1 += xs
            ListOfPoints.append((x1, y1, z1))
            if p1 >= 0:
                y1 += ys
                if not pixelPerfect:
                    if ListOfPoints[-1][1] != y1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                if not pixelPerfect:
                    if ListOfPoints[-1][2] != z1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz

    # Driving axis is Y-axis
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != y2:
            y1 += ys
            ListOfPoints.append((x1, y1, z1))
            if p1 >= 0:
                x1 += xs
                if not pixelPerfect:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                if not pixelPerfect:
                    if ListOfPoints[-1][2] != z1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz

    # Driving axis is Z-axis
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != z2:
            z1 += zs
            ListOfPoints.append((x1, y1, z1))
            if p1 >= 0:
                y1 += ys
                if not pixelPerfect:
                    if ListOfPoints[-1][1] != y1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                if not pixelPerfect:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
    return ListOfPoints


# -----------------------------------------------------------------------


def offset(N, pos1, pos2):
    """
    return A, perpendicular from [pos1;pos2] at N from pos1
    return B, perpendicular from [pos1;pos2] at -N from pos1
    return C, perpendicular from [pos2;pos1] at N from pos2
    return D, perpendicular from [pos2;pos1] at -N from pos2
    """
    A, B = mathPerpendicular(N * 2, pos1, pos2)
    C, D = mathPerpendicular(N * 2, pos2, pos1)
    return ([A, D], [B, C])


def mathPerpendicular(N, pos1, pos2):
    """
    2D Only
    """
    (x1, y1) = pos1
    (x2, y2) = pos2
    dx = x1 - x2
    dy = y1 - y2
    dist = sqrt(dx * dx + dy * dy)
    dx /= dist
    dy /= dist
    x3 = x1 + (N / 2) * dy
    y3 = y1 - (N / 2) * dx
    x4 = x1 - (N / 2) * dy
    y4 = y1 + (N / 2) * dx
    return ((round(x3), round(y3)), (round(x4), round(y4)))


########################### Bezier Functions ###########################


def smoothCurve(points, num_true_pts=40):
    """
    https://stackoverflow.com/questions/18962175/spline-interpolation-coefficients-of-a-line-curve-in-3d-space
    """

    x_sample = []
    y_sample = []
    z_sample = []

    for i in range(len(points)):
        x_sample.append(points[i][0])
        z_sample.append(points[i][1])
        y_sample.append(points[i][2])

    x_sample = np.array(x_sample)
    y_sample = np.array(y_sample)
    z_sample = np.array(z_sample)

    tck, u = interpolate.splprep([x_sample, y_sample, z_sample], s=2, k=2)
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0, 1, num_true_pts)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    # Visual Only
    # fig2 = plt.figure(2)
    # ax3d = fig2.add_subplot(111, projection='3d')
    # ax3d.plot(x_sample, y_sample, z_sample, 'r*')
    # ax3d.plot(x_knots, y_knots, z_knots, 'go')
    # ax3d.plot(x_fine, y_fine, z_fine, 'r')
    # fig2.show()
    # plt.show()

    x = x_fine.tolist()
    z = y_fine.tolist()
    y = z_fine.tolist()

    for i in x:
        i = round(i)
    for i in y:
        i = round(i)
    for i in z:
        i = round(i)

    # # Ingame Demo
    # for i in range(len(x)-1):
    #     setLine('blue_concrete', (x[i], y[i], z[i]), (x[i+1], y[i+1], z[i+1]))
    #     '''
    #     paralelle = offset (2, (x[i], z[i]), (x[i+1], z[i+1]))
    #     setLine('blue_concrete', (paralelle[0][0][0], y[i], paralelle[0][0][1]), (paralelle[0][1][0], y[i+1], paralelle[0][1][1]))
    #     setLine('red_concrete', (paralelle[1][0][0], y[i], paralelle[1][0][1]), (paralelle[1][1][0], y[i+1], paralelle[1][1][1]))
    #     '''
    # ###

    # for i in range(len(x)):
    #     setBlock('red_concrete', (x[i], y[i]+1, z[i]))

    # line0, line1 = smoothCurveOffset(x,y,z, N=10)
    # for i in range(len(line0)-1):
    #     setLineRandom('blue_concrete', 'blue_concrete', line0[i], line0[i+1], False)
    # for i in range(len(line1)-1):
    #     setLineRandom('blue_concrete', 'blue_concrete', line1[i], line1[i+1], False)
    # ###
    return (x, y, z)


def TESTsmoothRoads(points):
    """
    Preset road
    """

    # Calculating resolution depending of the distance
    distance = 0
    for i in range(len(points) - 1):
        distance += sqrt(
            ((points[i][0] - points[i + 1][0]) ** 2)
            + ((points[i][1] - points[i + 1][1]) ** 2)
            + ((points[i][2] - points[i + 1][2]) ** 2)
        )
    num_true_pts = round(distance / 10)

    # Calculation of the main line
    lineCenter0 = []
    x, y, z = smoothCurve(points, num_true_pts)
    for i in range(len(x) - 1):
        pos0 = x[i], y[i], z[i]
        pos1 = (x[i + 1], y[i + 1], z[i + 1])
        lineCenter0.extend(mathLine(pos0, pos1))
        setBlock("green_concrete", (x[i], y[i] + 1, z[i]))
    # lineCenter = noDuplicates
    lineCenter = []
    for i in lineCenter0:
        if i not in lineCenter:
            lineCenter.append(i)

    # Find what to do depending of the distance between the road and the ground
    listCenter = []
    for i in range(0, len(lineCenter), 7):
        groundDistance = lineCenter[i][1] - findGround(lineCenter[i])[1]

        if 0 <= groundDistance <= 7:  # remplir jusqu'au sol
            setBlock("red_concrete", lineCenter[i])
            listCenter.append(lineCenter[i])
        if 7 < groundDistance:  # générer pillier
            setBlock("blue_concrete", lineCenter[i])
            listCenter.append(lineCenter[i])
        if -7 <= groundDistance < 0:  # creuser
            listCenter.append(lineCenter[i])
        if -7 > groundDistance:  # tunnel
            listCenter.append(lineCenter[i])

    line0 = []
    line1 = []

    x = [listCenter[i][0] for i in range(len(listCenter))]
    y = [listCenter[i][1] for i in range(len(listCenter))]
    z = [listCenter[i][2] for i in range(len(listCenter))]

    for i in range(0, len(listCenter)):
        line0, line1 = smoothCurveOffset(x, y, z, N=5)
    for i in range(len(line0)):
        setBlock("blue_concrete", line0[i])
        setBlock(
            "blue_concrete", line1[i]
        )  # ICI calculer les lignes par section de routes pour déterminer ce qui doit y avoir en dessou ou au dessu. Pour les pilliers, les faire au niveau des calculs de la largeur.

    # Test
    # line0 = []
    # line1 = []
    # road = []

    # for i in range(10):
    #     lineA,lineB = (smoothCurveOffset(x,y,z, i/2))
    #     line0.append(lineA)
    #     line1.append(lineB)

    # for i in range(len(line0)):
    #     for j in range(len(line0[i])-1):
    #         road.append(mathLine(line0[i][j], line0[i][j+1], pixelPerfect=False))
    #         road.append(mathLine(line1[i][j], line1[i][j+1], pixelPerfect=False))

    # for i in range(len(road)):
    #     for j in range(len(road[i])):
    #         fillBlock('air', (road[i][j][0], road[i][j][1], road[i][j][2], road[i][j][0], road[i][j][1]+10, road[i][j][2]))

    # for i in range(len(road)):
    #     for j in range(len(road[i])):
    #         pos = findGround(road[i][j])
    #         fillBlock('stone', (road[i][j][0], road[i][j][1], road[i][j][2], pos[0], pos[1]-1, pos[2]))
    #         ### ICI on en était au pillier


def smoothRoads(points):

    # Calculating resolution depending of the distance
    distance = 0
    for i in range(len(points) - 1):
        distance += sqrt(
            ((points[i][0] - points[i + 1][0]) ** 2)
            + ((points[i][1] - points[i + 1][1]) ** 2)
            + ((points[i][2] - points[i + 1][2]) ** 2)
        )
    num_true_pts = round(distance / 10)

    # Calculation of the main line
    lineCenter0 = []
    x, y, z = smoothCurve(points, num_true_pts)
    for i in range(len(x) - 1):
        pos0 = x[i], y[i], z[i]
        pos1 = (x[i + 1], y[i + 1], z[i + 1])
        lineCenter0.extend(mathLine(pos0, pos1))

    # LineCenter = noDuplicates
    lineCenter = []
    for i in lineCenter0:
        if i not in lineCenter:
            lineCenter.append(i)

    # Offsetting
    listCenter = []
    for i in range(0, len(lineCenter), 7):
        listCenter.append(lineCenter[i])

    x = [listCenter[i][0] for i in range(len(listCenter))]
    y = [listCenter[i][1] for i in range(len(listCenter))]
    z = [listCenter[i][2] for i in range(len(listCenter))]

    N = 5
    line0 = []
    line1 = []

    for i in range(0, N * 2):
        lineA, lineB = smoothCurveOffset(x, y, z, i / 2)
        line0.append(lineA)
        line1.append(lineB)

    roadA = []
    roadB = []
    road1 = []
    road0 = []

    # "Parcing"
    for i in range(
        len(line0[0]) - 1
    ):  # line0[0][0],line0[1][0],line0[2][0]... line0[0][1],line0[1][1],line0[2][1]
        for j in range(len(line0)):
            roadA.append(
                mathLine(line0[j][i], line0[j][i + 1], pixelPerfect=False)
            )
            roadB.append(
                mathLine(line1[j][i], line1[j][i + 1], pixelPerfect=False)
            )
        road0.append(roadA)
        road1.append(roadB)
        roadA = []
        roadB = []

    eee = []
    for i in range(len(road0)):  # pour toute les parcelles
        # Find what to do depending of the distance between the road and the ground
        groundDistance = (
            listCenter[i + 1][1] - findGround(listCenter[i + 1])[1]
        )
        eee.append(groundDistance)

        if 0 <= groundDistance <= 7:  # remplir jusqu'au sol
            setBlock(
                "red_concrete",
                (listCenter[i][0], listCenter[i][1] + 3, listCenter[i][2]),
            )
        if 7 < groundDistance:  # générer pillier
            setBlock(
                "blue_concrete",
                (listCenter[i][0], listCenter[i][1] + 3, listCenter[i][2]),
            )
        if -7 <= groundDistance < 0:  # creuser
            pass
        if -7 > groundDistance:  # tunnel
            pass

        for j in range(len(road1[i])):  # pour toutes les lignes
            for k in range(len(road1[i][j])):  # pour tous les blocks
                setBlock("white_concrete", road1[i][j][k])
                if 0 <= groundDistance <= 7:  # remplir jusqu'au sol
                    fillBlock(
                        "black_concrete",
                        (
                            road1[i][j][k][0],
                            road1[i][j][k][1],
                            road1[i][j][k][2],
                            road1[i][j][k][0],
                            road1[i][j][k][1] - groundDistance,
                            road1[i][j][k][2],
                        ),
                    )
    print(eee)
    print(listCenter)
    # ICI améliroer la précision du fill et continuer les autres options
    # vérifier distance ground pour chaque pair qui encadre la parcelle. Si une des deux est == void alors ne rien mettre, si les 2 == fill alors fill


def smoothCurveOffset(
    x, y, z, N=5
):  # On peut améliorer la précision en trouvant l'arc intérieur et extérieur : relier les points de l'arc et non calculer leur milieu.
    """
    take 3D coordinates
    """
    lineA = []
    lineB = []
    line0 = []
    line1 = []

    # Offsetting
    for i in range(len(x) - 1):
        paralelle = offset(N, (x[i], z[i]), (x[i + 1], z[i + 1]))
        lineA.append(
            (
                (paralelle[0][0][0], y[i], paralelle[0][0][1]),
                (paralelle[0][1][0], y[i + 1], paralelle[0][1][1]),
            )
        )
        lineB.append(
            (
                (paralelle[1][0][0], y[i], paralelle[1][0][1]),
                (paralelle[1][1][0], y[i + 1], paralelle[1][1][1]),
            )
        )

    # First points
    line0.append(
        (round(lineA[0][0][0]), round(lineA[0][0][1]), round(lineA[0][0][2]))
    )
    line1.append(
        (round(lineB[0][0][0]), round(lineB[0][0][1]), round(lineB[0][0][2]))
    )

    # Middle of between segments
    for i in range(len(lineA) - 1):
        line0.append(
            (
                round((lineA[i][1][0] + lineA[i + 1][0][0]) / 2),
                round((lineA[i][1][1] + lineA[i + 1][0][1]) / 2),
                round((lineA[i][1][2] + lineA[i + 1][0][2]) / 2),
            )
        )
        line1.append(
            (
                round((lineB[i][1][0] + lineB[i + 1][0][0]) / 2),
                round((lineB[i][1][1] + lineB[i + 1][0][1]) / 2),
                round((lineB[i][1][2] + lineB[i + 1][0][2]) / 2),
            )
        )

    # Last points
    line0.append(
        (
            round(lineA[-1][1][0]),
            round(lineA[-1][1][1]),
            round(lineA[-1][1][2]),
        )
    )
    line1.append(
        (
            round(lineB[-1][1][0]),
            round(lineB[-1][1][1]),
            round(lineB[-1][1][2]),
        )
    )

    return (line0, line1)


############################ Lines Functions ###########################


def pixelPerfect(path):  # Revoir pour 3D
    """
    Transform a list of coordinates by deleting blocks
    """

    # NotPixelPerfect detection
    if len(path) == 1 or len(path) == 0:
        return path
    else:
        notPixelPerfect = []
        c = 0
        while c < len(path):
            if c > 0 and c + 1 < len(path):
                if (
                    (
                        path[c - 1][0] == path[c][0]
                        or path[c - 1][1] == path[c][1]
                    )
                    and (
                        path[c + 1][0] == path[c][0]
                        or path[c + 1][1] == path[c][1]
                    )
                    and path[c - 1][1] != path[c + 1][1]
                    and path[c - 1][0] != path[c + 1][0]
                ):
                    notPixelPerfect.append(path[c])
            c += 1

    # Double notPixelPerfect detection
    if len(notPixelPerfect) == 1 or len(notPixelPerfect) == 0:
        return notPixelPerfect
    else:
        d = 0
        while d < len(notPixelPerfect):
            if d + 1 < len(notPixelPerfect):
                if (
                    notPixelPerfect[d][0] == notPixelPerfect[d + 1][0]
                    and (notPixelPerfect[d][1] - notPixelPerfect[d + 1][1])
                    in {1, -1}
                ) or (
                    notPixelPerfect[d][1] == notPixelPerfect[d + 1][1]
                    and (notPixelPerfect[d][0] - notPixelPerfect[d + 1][0])
                    in {1, -1}
                ):
                    notPixelPerfect.remove(notPixelPerfect[d + 1])
            d += 1

    # Remove notPixelPerfect from path
    for i in range(len(notPixelPerfect)):
        path.remove(notPixelPerfect[i])

    return path


# -----------------------------------------------------------------------


def cleanLine(path):  # WORK BUT NOT ENDS : revoir pour 3D
    """
    clean and smooth a list of blocks coordinates:
    """

    i = 0
    while i < len(path):

        # for j in range(i-10,i):
        #     if i % 2 == 0:
        #         setBlock('green_stained_glass', (path[j][0], 112, path[j][1]))
        #     else:
        #         setBlock('blue_stained_glass', (path[j][0], 112, path[j][1]))
        # print("C")
        # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block

        if i + 3 < len(path):
            if (
                path[i][0] == path[i + 1][0]
                and path[i + 2][1] == path[i + 3][1]
            ):
                path.insert((i + 1), (path[i + 2][0], path[i + 1][1]))
                del path[i + 2]  # 2nd block
                del path[i + 2]  # 3rd block
                i -= 10
                print("A")
                continue
            elif (
                path[i][1] == path[i + 1][1]
                and path[i + 2][0] == path[i + 3][0]
            ):
                path.insert((i + 1), (path[i + 1][0], path[i + 2][1]))
                del path[i + 2]  # 2nd block
                del path[i + 2]  # 3rd block
                i -= 10
                print("B")
                continue

        # 1 block, 3 blocks, 1 block = 1 block, 2 blocks, 2 blocks
        if i - 1 >= 0 and i + 5 <= len(path):
            print("1")
            if (
                (
                    path[i + 1][1] == path[i + 2][1]
                    and path[i + 2][1] == path[i + 3][1]
                )
                and (
                    path[i + 1][1] != path[i][1]
                    and path[i + 3][1] != path[i + 4][1]
                )
                and (
                    path[i - 1][1] != path[i][1]
                    and path[i + 4][1] != path[i + 5][1]
                )
            ):
                path.insert((i + 1), (path[i + 1][0], path[i][1]))
                del path[i + 2]  # 2nd block
                i -= 10
                print("2")
                continue
            elif (
                (
                    path[i + 1][0] == path[i + 2][0]
                    and path[i + 2][0] == path[i + 3][0]
                )
                and (
                    path[i + 1][0] != path[i][0]
                    and path[i + 3][0] != path[i + 4][0]
                )
                and (
                    path[i - 1][0] != path[i][0]
                    and path[i + 4][0] != path[i + 5][0]
                )
            ):
                path.insert((i + 1), (path[i][0], path[i + 1][1]))
                del path[i + 2]  # 2nd block
                i -= 10
                print("3")
                continue

        i += 1
    return path


############################ Roads Generator ###########################


def worldtrade2(pos1, pos2, blockBase, blockGlass):
    """
    AI is creating summary for worldtrade2

    Args:
        pos1 ([type]): [description]
        pos2 ([type]): [description]
        blockBase ([type]): [description]
        blockGlass ([type]): [description]
    """
    # Init
    if pos1 == pos2:
        return None

    if pos1[1] > pos2[1]:
        yBot = pos2[1]
        yTop = pos1[1]
    else:
        yBot = pos1[1]
        yTop = pos2[1]

    base = wolrdMaxHeight

    if pos1[0] < pos2[0]:
        stepX = 1
    else:
        stepX = -1

    if pos1[2] < pos2[2]:
        stepZ = 1
    else:
        stepZ = -1

    # Center
    center = ((pos1[0] + pos2[0]) / 2, (pos1[2] + pos2[2]) / 2)

    # Base
    for x in range(pos1[0], pos2[0], stepX):
        for z in range(pos1[2], pos2[2], stepZ):
            ground = findGround((x, yBot, z))[1]
            if ground < base:
                base = ground

    fillBlock(blockBase, (pos1[0], yBot, pos1[2], pos2[0], base, pos2[2]))

    # Façades
    lineBot = []
    lineBot.append(
        mathLine((pos1[0], yBot, pos1[2]), (pos1[0], yBot, pos2[2]))
    )
    lineBot.append(
        mathLine((pos1[0], yBot, pos1[2]), (pos2[0], yBot, pos1[2]))
    )
    lineBot.append(
        mathLine((pos2[0], yBot, pos2[2]), (pos1[0], yBot, pos2[2]))
    )
    lineBot.append(
        mathLine((pos2[0], yBot, pos2[2]), (pos2[0], yBot, pos1[2]))
    )

    # Diagonal
    diag = []
    diag.append(mathLine((pos1[0], yBot, pos1[2]), (pos1[0], yTop, center[1])))
    diag.append(mathLine((pos1[0], yBot, pos1[2]), (center[0], yTop, pos1[2])))
    diag.append(mathLine((pos1[0], yBot, pos2[2]), (pos1[0], yTop, center[1])))
    diag.append(mathLine((pos1[0], yBot, pos2[2]), (center[0], yTop, pos2[2])))
    diag.append(mathLine((pos2[0], yBot, pos1[2]), (pos2[0], yTop, center[1])))
    diag.append(mathLine((pos2[0], yBot, pos1[2]), (center[0], yTop, pos1[2])))
    diag.append(mathLine((pos2[0], yBot, pos2[2]), (pos2[0], yTop, center[1])))
    diag.append(mathLine((pos2[0], yBot, pos2[2]), (center[0], yTop, pos2[2])))

    for i in range(0, len(diag), 2):
        for j in range(len(diag[i])):
            setLine(blockGlass, diag[i][j], diag[i + 1][j])

    # Floors
    floors = []
    stage = yBot
    while stage + 7 < yTop:
        temp = []
        stage += 7
        for i in range(len(diag)):
            temp.append(diag[i][stage])
        floors.append(temp)

    floor = []
    for i in range(len(floors)):
        for j in range(0, len(floors[i]), 2):
            floor.append(mathLine(floors[i][j], floors[i][j + 1]))

    for i in range(0, len(floor), 2):
        for j in range(len(floor[i])):
            a, b, c = floor[i][j]
            d, e, f = floor[i + 1][j]
            fillBlock(blockBase, (a, b, c, d, e, f))

    # Floors
    diag = []
    diag.append(mathLine((pos1[0], yBot, pos1[2]), (center[0], yTop, pos1[2])))
    diag.append(mathLine((pos1[0], yBot, pos2[2]), (center[0], yTop, pos1[2])))
    diag.append(mathLine((pos2[0], yBot, pos1[2]), (center[0], yTop, pos2[2])))
    diag.append(mathLine((pos2[0], yBot, pos2[2]), (center[0], yTop, pos2[2])))

    floors = []
    stage = yBot
    while stage + 7 < yTop:
        temp = []
        stage += 7
        for i in range(len(diag)):
            temp.append(diag[i][stage])
        floors.append(temp)

    floor = []
    for i in range(len(floors)):
        for j in range(0, len(floors[i]), 2):
            floor.append(mathLine(floors[i][j], floors[i][j + 1]))

    for i in range(0, len(floor), 2):
        for j in range(len(floor[i])):
            a, b, c = floor[i][j]
            d, e, f = floor[i + 1][j]
            fillBlock(blockBase, (a, b, c, d, e, f))

    # Lines
    diag = []
    diag.append(mathLine((pos1[0], yBot, pos1[2]), (pos1[0], yTop, center[1])))
    diag.append(mathLine((pos1[0], yBot, pos2[2]), (pos1[0], yTop, center[1])))
    diag.append(mathLine((pos1[0], yBot, pos1[2]), (center[0], yTop, pos1[2])))
    diag.append(mathLine((pos2[0], yBot, pos1[2]), (center[0], yTop, pos1[2])))
    diag.append(mathLine((pos1[0], yBot, pos2[2]), (center[0], yTop, pos2[2])))
    diag.append(mathLine((pos2[0], yBot, pos2[2]), (center[0], yTop, pos2[2])))
    diag.append(mathLine((pos2[0], yBot, pos1[2]), (pos2[0], yTop, center[1])))
    diag.append(mathLine((pos2[0], yBot, pos2[2]), (pos2[0], yTop, center[1])))

    # Structures

    for i in range(0, len(diag), 2):
        for j in range(len(diag[i])):
            a, b, c = diag[i][j]
            d, e, f = diag[i + 1][j]
            fillBlock(blockGlass, (a, b, c, d, e, f))

    for i in range(len(diag)):
        for j in range(len(diag[i])):
            setBlock(blockBase, diag[i][j])


def worldtrade(pos1, pos2, blockBase, blockGlass):
    """
    Draw a worldtradeilateral on pos1 and pos2

    Args:
        pos1 ([type]): [description]
        pos2 ([type]): [description]
        blockBase ([type]): [description]
        blockGlass ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Init
    if pos1 == pos2:
        return None

    if pos1[1] > pos2[1]:
        yBot = pos2[1]
        yTop = pos1[1]
    else:
        yBot = pos1[1]
        yTop = pos2[1]

    base = wolrdMaxHeight

    if pos1[0] < pos2[0]:
        stepX = 1
    else:
        stepX = -1

    if pos1[2] < pos2[2]:
        stepZ = 1
    else:
        stepZ = -1

    # Center
    center = ((pos1[0] + pos2[0]) / 2, (pos1[2] + pos2[2]) / 2)

    # Base
    for x in range(pos1[0], pos2[0], stepX):
        for z in range(pos1[2], pos2[2], stepZ):
            ground = findGround((x, yBot, z))[1]
            if ground < base:
                base = ground

    fillBlock(blockBase, (pos1[0], yBot, pos1[2], pos2[0], base, pos2[2]))

    # Façades
    lineBot = []
    lineBot.append(
        mathLine((pos1[0], yBot, pos1[2]), (pos1[0], yBot, pos2[2]))
    )
    lineBot.append(
        mathLine((pos1[0], yBot, pos1[2]), (pos2[0], yBot, pos1[2]))
    )
    lineBot.append(
        mathLine((pos2[0], yBot, pos2[2]), (pos1[0], yBot, pos2[2]))
    )
    lineBot.append(
        mathLine((pos2[0], yBot, pos2[2]), (pos2[0], yBot, pos1[2]))
    )

    for i in range(len(lineBot)):
        for j in range(len(lineBot[i])):
            if i == 0:
                setLine(blockGlass, lineBot[i][j], (pos1[0], yTop, center[1]))
            if i == 1:
                setLine(blockGlass, lineBot[i][j], (center[0], yTop, pos1[2]))
            if i == 2:
                setLine(blockGlass, lineBot[i][j], (center[0], yTop, pos2[2]))
            if i == 3:
                setLine(blockGlass, lineBot[i][j], (pos2[0], yTop, center[1]))

    lineTop = []
    lineTop.append(
        mathLine((center[0], yTop, pos1[2]), (pos1[0], yTop, center[1]))
    )
    lineTop.append(
        mathLine((pos1[0], yTop, center[1]), (center[0], yTop, pos2[2]))
    )
    lineTop.append(
        mathLine((center[0], yTop, pos2[2]), (pos2[0], yTop, center[1]))
    )
    lineTop.append(
        mathLine((pos2[0], yTop, center[1]), (center[0], yTop, pos1[2]))
    )

    for i in range(len(lineTop)):
        for j in range(len(lineTop[i])):
            if i == 0:
                setLine(blockGlass, lineTop[i][j], (pos1[0], yBot, pos1[2]))
            if i == 1:
                setLine(blockGlass, lineTop[i][j], (pos1[0], yBot, pos2[2]))
            if i == 2:
                setLine(blockGlass, lineTop[i][j], (pos2[0], yBot, pos2[2]))
            if i == 3:
                setLine(blockGlass, lineTop[i][j], (pos2[0], yBot, pos1[2]))


def skyscrapers(pos1, pos2, blockBase, blockGlass, blockFloor):
    """
    only impair
    """

    # Init
    if pos1 == pos2:
        return None

    if pos1[1] > pos2[1]:
        yBot = pos2[1]
        yTop = pos1[1]
    else:
        yBot = pos1[1]
        yTop = pos2[1]

    base = wolrdMaxHeight

    if pos1[0] < pos2[0]:
        stepX = 1
    else:
        stepX = -1

    if pos1[2] < pos2[2]:
        stepZ = 1
    else:
        stepZ = -1

    # Base
    # for x in range(pos1[0], pos2[0], stepX):
    #     for z in range(pos1[2], pos2[2], stepZ):
    #         ground = findGround((x,yBot,z))[1]
    #         if ground < base:
    #             base = ground

    # fillBlock(blockBase, (pos1[0], yBot, pos1[2], pos2[0], base, pos2[2]))

    # Façades
    for zPattern in range(pos1[2] + stepZ, pos2[2], stepZ * 2):
        fillBlock(
            blockBase,
            (pos1[0] + stepX, yBot, zPattern, pos1[0], yTop, zPattern),
        )
    for zPattern in range(pos1[2] + stepZ * 2, pos2[2], stepZ * 2):
        fillBlock(
            blockGlass,
            (
                pos1[0] + stepX,
                yBot + 1,
                zPattern,
                pos1[0] + stepX,
                yTop,
                zPattern,
            ),
        )
    for xPattern in range(pos1[0] + stepX, pos2[0], stepX * 2):
        fillBlock(
            blockBase,
            (xPattern, yBot, pos1[2] + stepZ, xPattern, yTop, pos1[2]),
        )
    for xPattern in range(pos1[0] + stepX * 2, pos2[0], stepX * 2):
        fillBlock(
            blockGlass,
            (
                xPattern,
                yBot + 1,
                pos1[2] + stepZ,
                xPattern,
                yTop,
                pos1[2] + stepZ,
            ),
        )

    for zPattern in range(pos1[2] + stepZ, pos2[2], stepZ * 2):
        fillBlock(
            blockBase,
            (pos2[0] - stepX, yBot, zPattern, pos2[0], yTop, zPattern),
        )
    for zPattern in range(pos1[2] + stepZ * 2, pos2[2], stepZ * 2):
        fillBlock(
            blockGlass,
            (
                pos2[0] - stepX,
                yBot + 1,
                zPattern,
                pos2[0] - stepX,
                yTop,
                zPattern,
            ),
        )
    for xPattern in range(pos1[0] + stepX, pos2[0], stepX * 2):
        fillBlock(
            blockBase,
            (xPattern, yBot, pos2[2] - stepZ, xPattern, yTop, pos2[2]),
        )
    for xPattern in range(pos1[0] + stepX * 2, pos2[0], stepX * 2):
        fillBlock(
            blockGlass,
            (
                xPattern,
                yBot + 1,
                pos2[2] - stepZ,
                xPattern,
                yTop,
                pos2[2] - stepZ,
            ),
        )
        # for z in range(pos1[2]+stepZ, pos2[2]-stepZ, stepZ):

    # Stages
    stage = yBot
    while stage + 7 < yTop:
        stage += 7
        fillBlock(
            blockFloor,
            (
                pos1[0] + stepX,
                stage,
                pos1[2] + stepZ,
                pos2[0] - stepX,
                stage - 1,
                pos2[2] - stepZ,
            ),
        )


def hyperions(pos):
    (x, y, z) = pos
    # points = np.array([[x+20, y, z],[x, y, z+15],[x-30, y, z],[x, y, z-20],[x+20, y, z]])
    points = np.array(
        [
            [x + 15, y, z],
            [x, y, z + 30],
            [x - 35, y, z],
            [x, y, z - 15],
            [x + 15, y, z],
        ]
    )
    smoothRoads(points)


def curves(points):

    # Calculating resolution depending of the distance
    distance = 0
    for i in range(len(points) - 1):
        distance += sqrt(
            ((points[i][0] - points[i + 1][0]) ** 2)
            + ((points[i][1] - points[i + 1][1]) ** 2)
            + ((points[i][2] - points[i + 1][2]) ** 2)
        )
    num_true_pts = round(distance / 10)

    # Calculation of the main line
    lineCenter0 = []
    x, y, z = smoothCurve(points, num_true_pts)
    for i in range(len(x) - 1):
        pos0 = x[i], y[i], z[i]
        pos1 = (x[i + 1], y[i + 1], z[i + 1])
        lineCenter0.extend(mathLine(pos0, pos1, pixelPerfect=False))

    # LineCenter = noDuplicates
    lineCenter = []
    for i in lineCenter0:
        if i not in lineCenter:
            lineCenter.append(i)

    return lineCenter


def building(pos1, pos2, pos3, pos4, block):
    print("t")
    line = mathLine(pos1, pos3)
    points = np.array([pos1, pos2, pos3])
    curve = curves(points)

    curve2 = []
    count = 0
    ratio = round(len(curve) / len(line))
    for i in range(len(curve)):
        if count >= ratio:
            count += 1
        points = np.array([curve[i], pos4, line[count]])
        curve2.append(curves(points))

    curve2 = list(curve2)

    for i in range(len(curve2)):
        for j in range(len(curve2[i])):
            setBlock(block, curve2[i][j])


############################## Executions ##############################

# setLine("blue_concrete", (3444, 69, -1324), (3394, 95, -1360), pixelPerfect=True)
a = 0
# points = [[3352, 75+a, -1330],[3352, 80+a, -1301],[3381, 85+a, -1301], [3381, 90+a, -1330],[3352, 95+a, -1330]]
# points = np.array([[3317, 80, -1743],[3330, 85, -1717],[3315,80, -1692],[3281, 75, -1712],[3308, 80, -1726],[3340, 80, -1735],[3347, 80, -1748],[3273, 80, -1794]])

# Grande route
# points = np.array([[3517, 83, -1267],[3551, 86, -1278],[3598, 87, -1310],[3632, 82, -1308],[3651, 84, -1293],[3687, 84, -1286],[3728, 85, -1304]])

# Grande route dérivation
# points = np.array([[3598, 87, -1310],[3624, 84, -1308],[3643, 73, -1327],[3649, 71, -1343],[3671, 66, -1368],[3688, 63, -1394],[3716, 69, -1413],[3761, 68, -1432],[3779, 74, -1467],[3773, 80, -1495],[3743, 83, -1540]])

# points = np.array([[3687, 144, -1526], [3613, 164, -1582], [3564, 165, -1554], [3528, 169, -1600]])
# points = np.array([[6916, 240, 1554],[6893, 230, 1488],[6847, 235, 1440],[6807, 245, 1390]])


# points = np.array([[6797, 145, 1394],[6837, 168, 1498],[6855, 174, 1564],[6963, 136, 1455]])

# pont montagne
# points = np.array([[6838, 85, 1516],[6878, 89, 1517],[6912, 87, 1518],[6926, 90, 1528], [6952, 89, 1548], [6992, 85, 1584]])
# points = np.array([[6838, 86, 1516],[6854, 83, 1537], [6885, 78, 1562], [6911, 79, 1577], [7014, 92, 1595]])
# points = np.array([[6940, 104, 1701],[6960, 101, 1700],[6973, 92, 1680],[6982, 85, 1666],[6997, 83, 1645],[7019, 86, 1616],[7032, 93, 1604],[6957, 115, 1646],[7043, 125, 1673],[7055, 150, 1650]])

# points = np.array([[-66, 69, 63],[-44, 71, 14],[18, 83, -19]])
# setLine('spruce_planks', (-6, 73, 83), (13, 70, -17), False)

# smoothRoads(points)

# hyperions((48, 190, 75))

# skyscrapers((320, 100, -222), (300, 70, -200), "white_concrete", "gray_stained_glass_pane", "gray_concrete")
# skyscrapers((266, 150, -239), (234, 73,-275), "white_concrete", "gray_stained_glass_pane", "gray_concrete")
# skyscrapers((399, 63, -285), (369, 200, -253), "white_concrete", "gray_stained_glass_pane", "gray_concrete")
# findGround((6953, 203, 1537))

# points = np.array([[-66, 69, 63],[-44, 71, 14],[18, 83, -19]])

# building((70, 4, -10), (34, 4, 0), (73, 4, -69), (51, 34, -35), "stone")
# skyscrapers((181, 4, -95), (217, 50, -135), "white_concrete", "gray_stained_glass_pane", "gray_concrete")
worldtrade2(
    (391, 4, -3),
    (391 + 50, 150, -3 + 50),
    "white_concrete",
    "light_blue_stained_glass",
)
