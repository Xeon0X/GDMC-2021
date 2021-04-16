from math import sqrt
from math import pi
from math import cos, sin
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


def line(xyz1, xyz2, pixelPerfect=True):
    """
    Calculate a line between two points in 3D space.

    https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/

    Args:
        xyz1 (tuple): First coordinates.
        xyz2 (tuple): Second coordinates.
        pixelPerfect (bool, optional): Blocks will be placed diagonally,
        not side by side if pixelPerfect is True. Defaults to True.

    Returns:
        list: List of blocks.
    """
    (x1, y1, z1) = xyz1
    (x2, y2, z2) = xyz2
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


def offset(distance, xy1, xy2):
    """
    Compute the coordinates of perpendicular points from two points. 2D
    only.

    Args:
        distance (int): Distance from the line[xy1;xy2] of the
        perpendicular points.
        xy1 (tuple): First position.
        xy2 (tuple): Second position.

    Returns:
        tuple: The coordinates of perpendicular points.
        A: Perpendicular from [xy1;xy2] at distance from pos1.
        B: perpendicular from [xy1;xy2] at -distance from pos1.
        C: perpendicular from [xy2;xy1] at distance from pos2.
        D: perpendicular from [xy2;xy1] at -distance from pos2.
    """
    A, B = perpendicular(distance * 2, xy1, xy2)
    C, D = perpendicular(distance * 2, xy2, xy1)
    return ([A, D], [B, C])


def perpendicular(distance, xy1, xy2):
    """
    Return a tuple of the perpendicular coordinates.

    Args:
        distance (int): Distance from the line[xy1;xy2].
        xy1 (tuple): First coordinates.
        xy2 (tuple): Second coordinates.

    Returns:
        tuple: Coordinates of the line length distance, perpendicular
        to [xy1; xy2] at xy1.
    """
    (x1, y1) = xy1
    (x2, y2) = xy2
    dx = x1 - x2
    dy = y1 - y2
    dist = sqrt(dx * dx + dy * dy)
    dx /= dist
    dy /= dist
    x3 = x1 + (distance / 2) * dy
    y3 = y1 - (distance / 2) * dx
    x4 = x1 - (distance / 2) * dy
    y4 = y1 + (distance / 2) * dx
    return ((round(x3), round(y3)), (round(x4), round(y4)))


def curve(points, number_true_pts=40, debug=False):
    """
    Returns a 3d curve.

    https://stackoverflow.com/questions/18962175/spline-interpolation-coefficients-of-a-line-curve-in-3d-space

    Args:
        points (np.array): Points where the curves should pass.
        number_true_pts (int, optional): Number of points to compute. Defaults to 40.
        debug (bool, optional): Just a visual graphic. Defaults to False.

    Returns:
        tuple: Tuple of list of each coordinate.
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
    u_fine = np.linspace(0, 1, number_true_pts)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    if debug:
        fig2 = plt.figure(2)
        ax3d = fig2.add_subplot(111, projection="3d")
        ax3d.plot(x_sample, y_sample, z_sample, "r*")
        ax3d.plot(x_knots, y_knots, z_knots, "go")
        ax3d.plot(x_fine, y_fine, z_fine, "r")
        fig2.show()
        plt.show()

    x = x_fine.tolist()
    z = y_fine.tolist()
    y = z_fine.tolist()

    for i in x:
        i = round(i)
    for i in y:
        i = round(i)
    for i in z:
        i = round(i)

    return x, y, z


def DELETEsmoothRoads(points):  # TODO: Delete but save cool parts before.
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
    x, y, z = curve(points, num_true_pts)
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
        line0, line1 = curveOffset(x, y, z, N=5)
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


def DELETEsmoothCurveSurface(points):  # TODO: Delete.
    print("test réussi")
    # TODO: Work in progress. Specific roads inside main?

    # Calculating resolution depending of the distance.
    distance = 0
    for i in range(len(points) - 1):
        distance += sqrt(
            ((points[i][0] - points[i + 1][0]) ** 2)
            + ((points[i][1] - points[i + 1][1]) ** 2)
            + ((points[i][2] - points[i + 1][2]) ** 2)
        )
    number_true_pts = round(distance / 10)

    # Calculation of the main line.
    lineCenter0 = []
    x, y, z = curve(points, number_true_pts)
    for i in range(len(x) - 1):
        pos0 = x[i], y[i], z[i]
        pos1 = (x[i + 1], y[i + 1], z[i + 1])
        lineCenter0.extend(line(pos0, pos1))

    # LineCenter = noDuplicates.
    lineCenter = []
    for i in lineCenter0:
        if i not in lineCenter:
            lineCenter.append(i)

    # Offsetting.
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
        lineA, lineB = curveOffset(x, y, z, i / 2)
        line0.append(lineA)
        line1.append(lineB)

    roadA = []
    roadB = []
    road1 = []
    road0 = []

    # Parsing.
    for i in range(len(line0[0]) - 1):
        # line0[0][0],line0[1][0],line0[2][0]... line0[0][1],line0[1][1],line0[2][1]
        for j in range(len(line0)):
            roadA.append(
                line(line0[j][i], line0[j][i + 1], pixelPerfect=False)
            )
            roadB.append(
                line(line1[j][i], line1[j][i + 1], pixelPerfect=False)
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
            minecraft.setBlock(
                "red_concrete",
                (listCenter[i][0], listCenter[i][1] + 3, listCenter[i][2]),
            )
        if 7 < groundDistance:  # générer pillier
            main.setBlock(
                "blue_concrete",
                (listCenter[i][0], listCenter[i][1] + 3, listCenter[i][2]),
            )
        if -7 <= groundDistance < 0:  # creuser
            pass
        if -7 > groundDistance:  # tunnel
            pass

        for j in range(len(road1[i])):  # pour toutes les lignes
            for k in range(len(road1[i][j])):  # pour tous les blocks
                main.setBlock("white_concrete", road1[i][j][k])
                if 0 <= groundDistance <= 7:  # remplir jusqu'au sol
                    main.fillBlock(
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


def curveOffset(x, y, z, distance=5):
    """
    Offset a curve.

    Args:
        x (list): List of x coordinates.
        y (list): List of y coordinates.
        z (list): List of z coordinates.
        distance (int, optional): Distance of offsetting. Defaults to 5.

    Returns:
        tuple: Lists of points from the upper curve and the lower curve.

    TODO:
        The accuracy can be improved by finding the inner and outer arc:
        connect the points of the arc and not calculate their
        middle.
    """
    lineA = []
    lineB = []
    line0 = []
    line1 = []

    # Offsetting
    for i in range(len(x) - 1):
        paralell = offset(distance, (x[i], z[i]), (x[i + 1], z[i + 1]))
        lineA.append(
            (
                (paralell[0][0][0], y[i], paralell[0][0][1]),
                (paralell[0][1][0], y[i + 1], paralell[0][1][1]),
            )
        )
        lineB.append(
            (
                (paralell[1][0][0], y[i], paralell[1][0][1]),
                (paralell[1][1][0], y[i + 1], paralell[1][1][1]),
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

    return line0, line1


def pixelPerfect(path):
    """
    Remove blocks that are side by side in the path. Keep the blocks
    that are in diagonal.

    Args:
        path (list): List of coordinates from a path.

    Returns:
        list: List cleaned.

    TODO:
        Add 3D.
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


def cleanLine(path):  # HERE
    """
    Clean and smooth a list of blocks.

    Args:
        path (list): List of blocks.

    Returns:
        list: List cleaned.

    TODO:
        Do not work perfecly since 16/04/2021.
        Add 3D. 3D Supported but not used. 16/04/2021.
        Add new patterns.
        Problem with i -= 10 : solved but not understand why. 16/04/2021.
    """

    pathTemp = []
    for i in path:
        if i not in pathTemp:
            pathTemp.append(i)
    path = pathTemp

    i = 0

    while i < len(path):

        # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block
        if i + 3 < len(path):
            if (
                path[i][0] == path[i + 1][0]
                and path[i + 2][-1] == path[i + 3][-1]
            ):
                if len(path[i + 1]) == 3:
                    path.insert(
                        (i + 1),
                        (path[i + 2][0], path[i + 2][1], path[i + 1][-1]),
                    )
                else:
                    path.insert((i + 1), (path[i + 2][0], path[i + 1][-1]))
                del path[i + 2]  # 2nd block
                del path[i + 2]  # 3rd block
                i -= 1
                continue
            elif (
                path[i][-1] == path[i + 1][-1]
                and path[i + 2][0] == path[i + 3][0]
            ):
                if len(path[i + 1]) == 3:
                    path.insert(
                        (i + 1),
                        (path[i + 1][0], path[i + 1][1], path[i + 2][-1]),
                    )
                else:
                    path.insert(
                        (i + 1),
                        (path[i + 1][0], path[i + 2][-1]),
                    )
                del path[i + 2]  # 2nd block
                del path[i + 2]  # 3rd block
                i -= 1
                continue

        # 1 block, 3 blocks, 1 block = 1 block, 2 blocks, 2 blocks
        if i - 1 >= 0 and i + 5 <= len(path):
            if (
                (
                    path[i + 1][-1] == path[i + 2][-1]
                    and path[i + 2][-1] == path[i + 3][-1]
                )
                and (
                    path[i + 1][-1] != path[i][-1]
                    and path[i + 3][-1] != path[i + 4][-1]
                )
                and (
                    path[i - 1][-1] != path[i][-1]
                    and path[i + 4][-1] != path[i + 5][-1]
                )
            ):
                if len(path[i]) == 3:
                    path.insert(
                        (i + 1), (path[i + 1][0], path[i + 1][1], path[i][-1])
                    )
                else:
                    path.insert((i + 1), (path[i + 1][0], path[i][-1]))
                del path[i + 2]  # 2nd block
                i -= 1
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
                if len(path[i]) == 3:
                    path.insert(
                        (i + 1), (path[i][0], path[i][1], path[i + 1][-1])
                    )
                else:
                    path.insert((i + 1), (path[i][0], path[i + 1][-1]))
                del path[i + 2]  # 2nd block
                i -= 1
                continue

        i += 1

    return path


def distance2D(A, B):  # TODO : Can be better.
    return sqrt((B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2)


def curveSurface(
    points, distance, resolution=7, pixelPerfect=False, factor=2
):  # HERE
    """
    Create a curve with a thickness.

    Args:
        points (numpy.ndarray): Points where the curve should go.
        distance (int): Thickness.
        resolution (int, optional): Number of blocks that separate each
        point to calculate parallel curves. 0 to use the points calculated to
        create the curve. Defaults to 7.
        pixelPerfect (bool, optional): True to avoid heaps. Defaults to
        False.
        factor (int, optional): Number of sub-line that will be
        calculated to avoid hole with coordinates. Defaults to 2.

    Returns:
        dict: Key 0 is the list of coordinates of the center line.
        Positive keys are lists of coordinates of lines on the right
        side, negative keys are for the left side.

    >>> curveSurface(
            np.array(
                [
                    [12, 248, -103],
                    [-5, 219, -85],
                    [-22, 205, -128],
                    [-51, 70, -240],
                    [40, 198, -166],
                    [19, 241, -102],
                    [-6, 62, -223],
                ]
            ),
            5,
            resolution=7,
        )
    """

    # Calculate resolution of the main curve depending of the total curve length.
    lenCurve = 0
    for i in range(len(points) - 1):
        lenCurve += sqrt(
            ((points[i][0] - points[i + 1][0]) ** 2)
            + ((points[i][1] - points[i + 1][1]) ** 2)
            + ((points[i][2] - points[i + 1][2]) ** 2)
        )
    number_true_pts = round(lenCurve / 10)

    # Calculate the main line.
    centerLineTemp = []
    X, Y, Z = curve(points, number_true_pts)
    for i in range(len(X) - 1):
        xyz0 = X[i], Y[i], Z[i]
        xyz1 = (X[i + 1], Y[i + 1], Z[i + 1])
        centerLineTemp.extend(line(xyz0, xyz1))

    # Clean the main line.
    centerLine = cleanLine(centerLineTemp)

    # Offset.
    centerPoints = []

    if resolution != 0:
        for i in range(0, len(centerLine), resolution):
            centerPoints.append(centerLine[i])
    else:
        for i in range(len(X)):
            centerPoints.append((X[i], Y[i], Z[i]))

    X = [centerPoints[i][0] for i in range(len(centerPoints))]
    Y = [centerPoints[i][1] for i in range(len(centerPoints))]
    Z = [centerPoints[i][2] for i in range(len(centerPoints))]

    rightPoints = []
    leftPoints = []

    for i in range(0, distance * factor):
        rightPoint, leftPoint = curveOffset(X, Y, Z, i / factor)
        rightPoints.append(rightPoint)
        leftPoints.append(leftPoint)

    # Creating lines on each side between each point.
    rightLine = []
    leftLine = []
    rightSide = []
    leftSide = []

    for i in range(len(rightPoints)):
        for j in range(len(rightPoints[i]) - 1):
            rightLine.extend(
                line(
                    rightPoints[i][j],
                    rightPoints[i][j + 1],
                    pixelPerfect,
                )
            )
        rightSide.append(rightLine)
        rightLine = []

    for i in range(len(leftPoints)):
        for j in range(len(leftPoints[i]) - 1):
            leftLine.extend(
                line(
                    leftPoints[i][j],
                    leftPoints[i][j + 1],
                    pixelPerfect,
                )
            )
        leftSide.append(leftLine)
        leftLine = []

    # else:  # Do not create lines. Points instead.
    #     for i in range(len(rightPoints)):
    #         for j in range(len(rightPoints[i])):
    #             rightLine.append(rightPoints[i][j])
    #         rightSide.append(rightLine)
    #         rightLine = []

    #     for i in range(len(leftPoints)):
    #         for j in range(len(leftPoints[i])):
    #             leftLine.append(leftPoints[i][j])
    #         leftSide.append(leftLine)
    #         leftLine = []

    # Returns. 0 is the center line, positive values ​​are lines on the
    # right, negative values ​​are lines on the left.
    smoothCurveSurfaceDict = {}
    smoothCurveSurfaceDict[0] = centerLine
    countLine = 0
    for l in rightSide:
        l = cleanLine(l)
        countLine += 1
        smoothCurveSurfaceDict[countLine] = l
    countLine = 0
    for l in leftSide:
        l = cleanLine(l)
        countLine -= 1
        smoothCurveSurfaceDict[countLine] = l

    return smoothCurveSurfaceDict


def getAngle(p0, p1, p2):
    """
    Compute angle (in degrees) for p0p1p2 corner.

    https://stackoverflow.com/questions/13226038/calculating-angle-between-two-vectors-in-python

    Args:
        p0 (numpy.ndarray: Points in the form of [x,y].
        p1 (numpy.ndarray: Points in the form of [x,y].
        p2 (numpy.ndarray: Points in the form of [x,y].

    Returns:
        float: Angle negative for counterclockwise angle, angle positive
        for counterclockwise angle.
    """
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    return np.degrees(angle)


def lineIntersection(line0, line1):
    """
    Find (or not) intersection between two lines.

    https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines

    Args:
        line0 (tuple): Tuple of tuple of coordinates.
        line1 (tuple): Tuple of tuple of coordinates.

    Returns:
        tuple: Coordinates.

    >>> lineIntersection(((0, 0), (0, 5)), ((2.5, 2.5), (-2.5, 2.5)))
    """
    xdiff = (line0[0][0] - line0[1][0], line1[0][0] - line1[1][0])
    ydiff = (line0[0][1] - line0[1][1], line1[0][1] - line1[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line0), det(*line1))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def circle_line_segment_intersection(
    circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9
):
    """
    Find the points at which a circle intersects a line-segment. This
    can happen at 0, 1, or 2 points.

    https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
    Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html

    Args:
        circle_center ([type]): The (x, y) location of the circle center.
        circle_radius ([type]): The radius of the circle.
        pt1 ([type]): The (x, y) location of the first point of the segment.
        pt2 ([type]): The (x, y) location of the second point of the segment.
        full_line (bool, optional): True to find intersections along
        full line - not just in the segment.  False will just return
        intersections within the segment. Defaults to True.
        tangent_tol ([type], optional): Numerical tolerance at which we decide the intersections are close enough to consider it a tangent. Defaults to 1e-9.

    Returns:
        list: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** 0.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (
                cx
                + (
                    big_d * dy
                    + sign * (-1 if dy < 0 else 1) * dx * discriminant ** 0.5
                )
                / dr ** 2,
                cy
                + (-big_d * dx + sign * abs(dy) * discriminant ** 0.5)
                / dr ** 2,
            )
            for sign in ((1, -1) if dy < 0 else (-1, 1))
        ]  # This makes sure the order along the segment is correct
        if (
            not full_line
        ):  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [
                (xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy
                for xi, yi in intersections
            ]
            intersections = [
                pt
                for pt, frac in zip(intersections, fraction_along_segment)
                if 0 <= frac <= 1
            ]
        if (
            len(intersections) == 2 and abs(discriminant) <= tangent_tol
        ):  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


def circle(xyC, r):
    """
    Can be used for circle or disc.

    Args:
        xyC (tuple): Coordinates of the center.
        r (int): Radius of the circle.

    Returns:
        dict: Keys are distance from the circle. Value is a list of all
        coordinates at this distance. 0 for a circle. Negative values for
        a disc, positive values for a hole.
    """
    area = (
        (round(xyC[0]) - round(r), round(xyC[1]) - round(r)),
        (round(xyC[0]) + round(r) + 1, round(xyC[1]) + round(r) + 1),
    )

    circle = {}
    for x in range(area[0][0], area[1][0]):
        for y in range(area[0][1], area[1][1]):
            d = round(distance2D((x, y), (xyC))) - r
            if circle.get(d) == None:
                circle[d] = []
            circle[d].append((x, y))
    return circle


def circleIntersections(xy0, r0, xy1, r1):
    # https://stackoverflow.com/questions/55816902/finding-the-intersection-of-two-circles
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    x0, y0 = xy0
    x1, y1 = xy1
    d = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return ((x3, y3), (x4, y4))


def InTriangle(p_test, p0, p1, p2):
    # https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle#:~:text=A%20simple%20way%20is%20to,point%20is%20inside%20the%20triangle.
    dX = p_test[0] - p0[0]
    dY = p_test[1] - p0[1]
    dX20 = p2[0] - p0[0]
    dY20 = p2[1] - p0[1]
    dX10 = p1[0] - p0[0]
    dY10 = p1[1] - p0[1]

    s_p = (dY20 * dX) - (dX20 * dY)
    t_p = (dX10 * dY) - (dY10 * dX)
    D = (dX10 * dY20) - (dY10 * dX20)

    if D > 0:
        return (s_p >= 0) and (t_p >= 0) and (s_p + t_p) <= D
    else:
        return (s_p <= 0) and (t_p <= 0) and (s_p + t_p) >= D


def circlePoints(xyC, r, n=100):
    # https://stackoverflow.com/questions/8487893/generate-all-the-points-on-the-circumference-of-a-circle
    points = [
        (cos(2 * pi / n * x) * r, sin(2 * pi / n * x) * r)
        for x in range(0, n + 1)
    ]

    for i in range(len(points)):
        points[i] = (
            points[i][0] + xyC[0],
            points[i][1] + xyC[1],
        )

    return points


def optimizedPath(coords, start=None):
    """
    This function finds the nearest point to a point
    coords should be a list in this format coords = [ [x1, y1], [x2, y2] , ...]
    # https://stackoverflow.com/questions/45829155/sort-points-in-order-to-have-a-continuous-curve-using-python
    """
    if start is None:
        start = coords[0]
    pass_by = coords
    path = [start]
    pass_by.remove(start)
    while pass_by:
        nearest = min(pass_by, key=lambda x: distance2D(path[-1], x))
        path.append(nearest)
        pass_by.remove(nearest)
    return path


def nearest(points, start):
    return min(points, key=lambda x: distance2D(start, x))
