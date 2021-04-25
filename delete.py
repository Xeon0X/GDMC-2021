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


def roadIntersection(line0, line1, y=140):  # TODO: Refactoring
    print("start")
    intersection = maths.lineIntersection(line0, line1)
    if intersection == None:
        return None

    # angle = maths.getAngle(line0[0], intersection, line1[-1])
    # StartDistance = 30 * abs(
    #     1 / (angle / 90)
    # )  # Set here the radius of the circle for a square angle.
    StartDistance = 30

    startCurvePoint = maths.circleLineSegmentIntersection(
        intersection, StartDistance, line0[0], intersection, fullLine=True
    )[0]
    endCurvePoint = maths.circleLineSegmentIntersection(
        intersection, StartDistance, line1[-1], intersection, fullLine=True
    )[0]

    perpendicular0 = maths.perpendicular(1000, startCurvePoint, intersection)[
        0
    ]  # Higher value for better precision
    perpendicular1 = maths.perpendicular(1000, endCurvePoint, intersection)[1]

    center = maths.lineIntersection(
        (perpendicular0, startCurvePoint), (perpendicular1, endCurvePoint)
    )
    print("start2")

    # distance = maths.distance2D(startCurvePoint, endCurvePoint)

    # centerTemp = maths.circleIntersections(
    #     startCurvePoint, distance / 2, endCurvePoint, distance / 2
    # )
    # center = ()
    # print("he", centerTemp, intersection)
    # for i in range(len(centerTemp)):
    #     print(centerTemp[i], intersection, i)
    #     if centerTemp[i] != intersection:
    #         center = centerTemp[i]
    # print("i", center)

    # main.setLine(
    #     "gray_concrete",
    #     (startCurvePoint[0], y - 1, startCurvePoint[1]),
    #     (center[0], y - 1, center[1]),
    # )
    # main.setLine(
    #     "gray_concrete",
    #     (endCurvePoint[0], y + 1, endCurvePoint[1]),
    #     (center[0], y + 1, center[1]),
    # )
    print("start3")
    # main.setBlock("red_concrete", (round(center[0]), y, round(center[1])))
    # main.setBlock("yellow_concrete", (perpendicular0[0], y, perpendicular0[1]))
    # main.setBlock("purple_concrete", (perpendicular1[0], y, perpendicular1[1]))
    # main.setBlock(
    #     "green_concrete",
    #     (round(startCurvePoint[0]), y + 1, round(startCurvePoint[1])),
    # )
    # main.setBlock(
    #     "pink_concrete",
    #     (round(endCurvePoint[0]), y + 1, round(endCurvePoint[1])),
    # )
    main.setLine(
        "white_concrete",
        (line0[0][0], y, line0[0][1]),
        (line0[1][0], y, line0[1][1]),
    )
    main.setLine(
        "white_concrete",
        (line1[0][0], y, line1[0][1]),
        (line1[1][0], y, line1[1][1]),
    )
    print("start4")

    d0 = maths.distance2D(startCurvePoint, center)
    d1 = maths.distance2D(endCurvePoint, center)

    print(d0, d1)
    # circle = maths.circle(center, round(d0))[0]
    circle = maths.circlePoints(center, round(d0), n=100)
    print("mmmm", circle)

    for i in circle:
        if maths.InTriangle(i, intersection, startCurvePoint, endCurvePoint):
            main.setBlock("orange_concrete", (i[0], y - 1, i[1]))  # Work ?

    points = []
    for i in circle:
        if maths.InTriangle(i, intersection, startCurvePoint, endCurvePoint):
            points.append((i[0], i[1]))

    startPoint = maths.nearest(points, startCurvePoint)
    print(startPoint)
    points = maths.optimizedPath(points, startPoint)

    points2 = []
    for i in points:
        points2.append((i[0], y, i[1]))

    main.setCurveSurface("stone", np.array(points2), 1)

    # print(maths.getAngle(intersection, endCurvePoint, center))
    # print(maths.getAngle(intersection, startCurvePoint, center))

    # def DELETEintersection(centerPoint, roads):  # (x, y, z), {}
    # # backroads : [{"coordinates": ((x, y, z)), "width": 3, "blocks":{"road_surface": {"andesite": 3, "stone": 6, "cobblestone": 1}, "median_strip": {"stone": 1}}}}
    # mainPoints = (
    #     roads.get("main")["coordinates"][0],
    #     centerPoint,
    #     roads.get("main")["coordinates"][1],
    # )
    # mainWidth = roads.get("main")["width"]
    # mainRoad = maths.curveSurface(
    #     np.array(mainPoints),
    #     mainWidth,
    #     resolution=0,
    #     start=mainWidth - 1,
    #     factor=1,
    #     returnLine=False,
    # )

    # backroadsRoad = []
    # for i in range(len(roads.get("backroads"))):
    #     backroadsPoints = (
    #         roads.get("backroads")[i]["coordinates"],
    #         centerPoint,
    #     )
    #     backroadsWidth = roads.get("backroads")[i]["width"]
    #     backroadsRoad.append(
    #         maths.curveSurface(
    #             np.array(backroadsPoints),
    #             backroadsWidth,
    #             resolution=0,
    #             start=backroadsWidth - 1,
    #             factor=1,
    #             returnLine=False,
    #         )
    #     )

    # intersections = []
    # for i in range(len(backroadsRoad)):
    #     for j in range(len(mainRoad[1]) - 1):
    #         line0 = backroadsRoad[i][-1][0], backroadsRoad[i][-1][-1]
    #         line1 = mainRoad[1][j], mainRoad[1][j + 1]
    #         intersection = maths.lineIntersection(line0, line1, fullLine=True)
    #         print(line0, line1)
    #         if intersection != None:
    #             intersections.append(((line1), (line0)))
    #             main.setBlock(
    #                 "yellow_concrete",
    #                 (
    #                     mainRoad[1][j][0],
    #                     mainRoad[1][j][1] + 2,
    #                     mainRoad[1][j][2],
    #                 ),
    #             )
    #             main.setBlock(
    #                 "white_concrete",
    #                 (
    #                     round(intersection[0]),
    #                     101,
    #                     round(intersection[1]),
    #                 ),
    #             )
    # print(intersections)
    # print(intersections[0][0], intersections[0][1])
    # roadIntersection(
    #     (
    #         (intersections[0][0][0][0], intersections[0][0][0][-1]),
    #         (intersections[0][0][1][0], intersections[0][0][1][-1]),
    #     ),
    #     (
    #         (intersections[0][1][1][0], intersections[0][1][1][-1]),
    #         (intersections[0][1][0][0], intersections[0][1][0][-1]),
    #     ),
    #     y=110,
    # )
    # roadIntersection(
    #     (
    #         (intersections[-1][0][1][0], intersections[-1][0][1][-1]),
    #         (intersections[-1][0][0][0], intersections[-1][0][0][-1]),
    #     ),
    #     (
    #         (intersections[-1][1][1][0], intersections[-1][1][1][-1]),
    #         (intersections[-1][1][0][0], intersections[-1][1][0][-1]),
    #     ),
    #     y=110,
    # )

    # for i in range(len(backroadsRoad)):
    #     for lane in backroadsRoad[i]:
    #         for xyz in backroadsRoad[i][lane]:
    #             main.setBlock("red_concrete", xyz)
    # for lane in mainRoad:
    #     for xyz in mainRoad[lane]:
    #         main.setBlock("purple_concrete", xyz)


def setCurveSurface(block, points, distance):  # TODO: Delete ?
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