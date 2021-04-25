import numpy as np
import maths
import math
import main
import random


road = {}


def highways(
    blocks, XZ, altitude, numberLanes, factor=4, destroy=False
):  # TODO: Refactoring to generate more roads based on dict.
    distance = (
        3
        + numberLanes
        * 4  # 3 is blocks in the middle + extremity, 4 is blocks per lane.
    )  # How many blocks for the width for the half of the road.

    curve = maths.curveSurface(
        np.array(XZ), distance, resolution=0, pixelPerfect=True, factor=factor
    )  # Points. For precision lines.

    baseLayer = maths.curveSurface(
        np.array(XZ),
        distance,
        resolution=0,
        pixelPerfect=False,
        factor=factor,
    )  # Lines. To avoid holes. Not precise. -1 because extremity not precise.

    for lane in baseLayer:  # Base. Not precise.
        for xyz in baseLayer[lane]:
            road_surface = blocks.get("road_surface")
            structure = blocks.get("structure")
            if road_surface == None:
                road_surface = "stone"
            else:
                main.setBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )  # Structure under the road.
                main.setBlock(
                    random.choices(
                        list(road_surface.keys()),
                        weights=road_surface.values(),
                        k=1,
                    )[0],
                    (xyz),
                )  # Surface road.
                main.fillBlock(
                    "air",
                    (
                        xyz[0],
                        xyz[1] + 1,
                        xyz[2],
                        xyz[0],
                        xyz[1] + 5,
                        xyz[2],
                    ),
                )  # Clean the top of the road.

    for lane in curve:  # Other materials. Precision lines.
        counterLines = 0  # For lines segmentation.
        for xyz in curve[lane]:
            if lane == 0:  # Middle.
                median_strip = blocks.get("median_strip")
                main.setBlock(
                    random.choices(
                        list(median_strip.keys()),
                        weights=median_strip.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] + 1, xyz[2]),
                )

            if lane == (factor * distance) or lane == (
                -factor * distance
            ):  # Extremity.
                median_strip = blocks.get("structure")
                main.setBlock(
                    random.choices(
                        list(median_strip.keys()),
                        weights=median_strip.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] + 1, xyz[2]),
                )
                main.setBlock(
                    random.choices(
                        list(median_strip.keys()),
                        weights=median_strip.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1], xyz[2]),
                )
                main.setBlock(
                    random.choices(
                        list(median_strip.keys()),
                        weights=median_strip.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )

            if lane == (factor / 2) + (factor) or lane == (-factor / 2) + (
                -factor
            ):  # Central lines.
                central_lines = blocks.get("central_lines")
                main.setBlock(
                    random.choices(
                        list(central_lines.keys()),
                        weights=central_lines.values(),
                        k=1,
                    )[0],
                    (xyz),
                )

            if lane == (factor / 2) + (
                factor * distance - factor * 2
            ) or lane == (-factor / 2) + (
                -factor * distance + factor * 2
            ):  # External lines.
                external_lines = blocks.get("external_lines")
                main.setBlock(
                    random.choices(
                        list(external_lines.keys()),
                        weights=external_lines.values(),
                        k=1,
                    )[0],
                    (xyz),
                )

            for l in range(2, numberLanes):
                if (lane == (factor * 5) * l - factor / 2) or (
                    lane == (-factor * 5) * l + factor / 2
                ):  # Lines.
                    counterLines += 1
                    if (counterLines % 4) != 0:
                        lines = blocks.get("lines")
                        main.setBlock(
                            random.choices(
                                list(lines.keys()),
                                weights=lines.values(),
                                k=1,
                            )[0],
                            (xyz),
                        )

            if (lane == (factor * 5) * 1 + factor / 2) or (
                lane == (-factor * 5) * 1 - factor / 2
            ):  # Lines.
                counterLines += 1
                if (counterLines % 4) != 0:
                    lines = blocks.get("lines")
                    main.setBlock(
                        random.choices(
                            list(lines.keys()),
                            weights=lines.values(),
                            k=1,
                        )[0],
                        (xyz),
                    )

    if destroy:
        for lane in baseLayer:  # Base. Not precise. # Can be better here.
            for xyz in baseLayer[lane]:
                no = []
                for i in range(factor):
                    no.append(i)
                if (
                    lane not in no
                    and lane != (factor * distance)
                    and lane != (-factor * distance)
                ):
                    if random.randint(0, 1) == 1:
                        road_top = blocks.get("road_top")
                        road_under_top = blocks.get("road_under_top")
                        if road_under_top == None:
                            break
                        else:
                            main.setBlock(
                                random.choices(
                                    list(road_under_top.keys()),
                                    weights=road_under_top.values(),
                                    k=1,
                                )[0],
                                (xyz[0], xyz[1], xyz[2]),
                            )
                        if road_top == None:
                            break
                        else:
                            block = random.choices(
                                list(road_top.keys()),
                                weights=road_top.values(),
                                k=1,
                            )[0]
                            main.setBlock(
                                str(block),
                                (xyz[0], xyz[1] + 1, xyz[2]),
                            )  # On the road.
                            main.setBlock(
                                str(block + "[half=upper]"),
                                (xyz[0], xyz[1] + 2, xyz[2]),
                            )


def DELETEintersection(centerPoint, roadsData):
    # Parsing dict.
    roadsTemp = []
    for i in range(len(roadsData)):
        roadsPoints = (roadsData[i].get("coordinates"), centerPoint)
        roadsWidth = roadsData[i].get("width")
        roadsTemp.append(
            maths.curveSurface(
                np.array(roadsPoints),
                roadsWidth,
                resolution=0,
                start=roadsWidth - 1,
                factor=1,
                returnLine=False,
            )
        )

    # Be sure that all the points are in a correct order. Take only the
    # first points because the last are the at the center.
    points = []
    for i in range(len(roadsTemp)):
        for j in range(-1, 2):  # -1: left, 0: middle, 1: right.
            points.append((roadsTemp[i][j][0]))
    roadsSorted = maths.sortRotation(points)

    # Rearrange coordinates to associate each sorted coordinate with the
    # other coordinate that forms the line. Only left and right.
    roads = []
    for pointsSorted in roadsSorted:
        for k in range(len(roadsTemp)):
            for j in range(-1, 2):  # -1: left, 0: middle, 1: right
                if pointsSorted in roadsTemp[k][j] and j != 0:
                    roads.append(roadsTemp[k][j])

    # Compute the intersection for all the roads. Only left and right.
    intersections = []
    print(roads)
    for i in range(0, len(roads), 2):
        print(i)
        line0 = roads[i]
        line1 = roads[i - 1]
        main.setLine("white_concrete", line0[0], line0[1])
        main.setLine("red_concrete", line1[0], line1[1])
        intersectionPoints = maths.curveCornerIntersection(line0, line1, 10)
        # 2d to 3d.
        for i in range(len(intersectionPoints)):
            intersectionPoints[i] = (
                intersectionPoints[i][0],
                185,
                intersectionPoints[i][1],
            )
        print(intersectionPoints)
        if intersection != None:
            generate = Roads(
                blocky,
                intersectionPoints,
                {
                    "heightData": "heightmap / inputCoordinates",
                    "lanes": {
                        0: {"type": simpleLane, "centerDistance": -11},
                        1: {"type": simpleLane, "centerDistance": 11},
                    },
                },
            )
            generate.lanes([], setLanes=True)
            # for i in range(len(intersectionPoints)):
            #     main.setBlock(
            #         "white_concrete",
            #         (
            #             round(intersectionPoints[i][0]),
            #             185,
            #             round(intersectionPoints[i][1]),
            #         ),
            #     )


def cleanLanes(lanes):
    cleanLanes = {}
    for lane in lanes:
        for xyz in lanes[lane]:
            if xyz not in cleanLanes.values():
                if cleanLanes.get(lane) == None:
                    cleanLanes[lane] = []
                cleanLanes[lane].append(xyz)
    return cleanLanes


def simpleLane(blocks, XYZ):
    roadMarkings = maths.curveSurface(
        np.array(XYZ), 4, resolution=0, pixelPerfect=True, factor=8
    )
    roadMarkings = cleanLanes(roadMarkings)

    roadSurface = maths.curveSurface(
        np.array(XYZ),
        4,
        resolution=0,
        pixelPerfect=False,
        factor=8,
    )
    roadSurface = cleanLanes(roadSurface)

    road_surface = blocks.get("road_surface")
    structure = blocks.get("structure")
    for lane in roadSurface:
        for xyz in roadSurface[lane]:
            main.setBlock(
                random.choices(
                    list(road_surface.keys()),
                    weights=road_surface.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1], xyz[2]),
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )

    external_lines = blocks.get("external_lines")
    central_lines = blocks.get("central_lines")
    counterSegments = 0
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == (8 * 4) or lane == (-8 * 4):
                main.setBlock(
                    random.choices(
                        list(external_lines.keys()),
                        weights=external_lines.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1], xyz[2]),
                )
            if lane == 0:
                counterSegments += 1
                if counterSegments % 4 != 0:
                    main.setBlock(
                        random.choices(
                            list(central_lines.keys()),
                            weights=central_lines.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )


def DELETE2intersection(blocks, XYZ, roadsData):
    centerPoint = XYZ[0]
    sidePoints = maths.sortRotation([XYZ[i] for i in range(1, len(XYZ))])
    lanes = []
    for i in range(0, len(sidePoints)):
        path = Roads(blocks, (sidePoints[i], centerPoint), roadsData)
        # path.setLanes([])
        lanes.append(path.getLanes([]))

    for i in range(len(lanes)):
        line0 = lanes[i][max(lanes[i])]
        line1 = lanes[i - 1][min(lanes[i - 1])]
        intersectionPointsTemp = maths.curveCornerIntersection(
            line0, line1, 10
        )
        for i in range(len(intersectionPointsTemp)):
            intersectionPointsTemp[i] = (
                round(intersectionPointsTemp[i][0]),
                round(intersectionPointsTemp[i][1]),
            )
        intersectionPoints = []
        intersectionPoints.append(line0[0])
        noDuplicates = []
        for i in range(len(intersectionPointsTemp)):
            if intersectionPointsTemp[i] not in noDuplicates:
                noDuplicates.append(intersectionPointsTemp[i])
                intersectionPoints.append(
                    (
                        intersectionPointsTemp[i][0],
                        150,
                        intersectionPointsTemp[i][1],
                    )
                )
                main.setBlock(
                    "purple_concrete",
                    (
                        round(intersectionPoints[i][0]),
                        151,
                        round(intersectionPoints[i][-1]),
                    ),
                )
        intersectionPoints.append(line1[0])

        pathTemp = Roads(blocks, (intersectionPoints), roadsData)
        pathTemp.setLanes([])
        del pathTemp

        ## Test
        main.setLine("red_concrete", line0[0], line0[1])
        main.setLine("blue_concrete", line1[0], line1[1])

    print(lanes)


class Roads:
    def __init__(self, blocks, XYZ, roadsData):
        self.blocks = blocks
        self.XYZ = XYZ
        self.roadsData = roadsData

        # Find the center of each lane and compute the offset
        # coordinates.
        self.lanesXYZ = {}
        for __, i in enumerate(self.roadsData["lanes"]):
            laneCenterDistance = self.roadsData["lanes"][i]["centerDistance"]
            self.lanesXYZ[i] = maths.curveSurface(
                np.array(XYZ),
                abs(laneCenterDistance),
                resolution=0,
                pixelPerfect=True,
                factor=1,
                start=abs(laneCenterDistance) - 1,
                returnLine=False,
            )
            # Because this function return 0: middle, 1: right -1: left,
            # we only take the desired side.
            if laneCenterDistance == 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][0]
            if laneCenterDistance > 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][1]
            if laneCenterDistance < 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][-1]

    def setLanes(self, lanes):
        # Create all the lanes depending of the function name. Each
        # function is specialized into generate one type of lane.
        for __, i in enumerate(self.roadsData["lanes"]):
            if i in lanes or lanes == []:
                self.roadsData["lanes"][i]["type"](
                    self.blocks, np.array(self.lanesXYZ[i])
                )

    def getLanes(self, lanes):
        # Return the points that forms the each lane.
        lanesDict = {}
        for __, i in enumerate(self.roadsData["lanes"]):
            if i in lanes or lanes == []:
                lanesDict[i] = self.lanesXYZ[i]
        return lanesDict


blocky = {
    "road_surface": {
        "black_concrete": 3,
        "coal_block": 1,
        "black_concrete_powder": 2,
    },
    "median_strip": {"stone": 1},
    "structure": {"stone": 1},
    "central_lines": {"yellow_concrete": 3, "yellow_concrete_powder": 1},
    "external_lines": {"white_concrete": 3, "white_concrete_powder": 1},
    "lines": {"white_concrete": 3, "white_concrete_powder": 1},
    "road_under_top": {
        "grass_block": 15,
        "coarse_dirt": 3,
        "podzol": 1,
        "stone_slab": 2,
    },
    "road_top": {
        "grass": 4,
        "poppy": 1,
        "dandelion": 1,
        "fern": 3,
        "tall_grass": 3,
        "large_fern": 3,
        "air": 8,
    },
}

test = {
    "lanes": {
        -1: {"type": simpleLane, "centerDistance": -11},
        1: {"type": simpleLane, "centerDistance": 11},
        2: {"type": simpleLane, "centerDistance": 17},
    },
}

intersection(
    blocky,
    [(150, 150, 15), (200, 150, 0), (100, 150, -20), (140, 150, 60)],
    test,
)

# a = Roads(
#     blocky,
#     [(0, 78 + 30, -2), (102, 80 + 30, -13), (127, 85 + 30, 11)],
#     {
#         "heightData": "heightmap / inputCoordinates",
#         "lanes": {
#             0: {"type": simpleLane, "centerDistance": -11},
#             1: {"type": simpleLane, "centerDistance": 11},
#         },
#     },
# )

# a.lanes([], setLanes=True)


# highways(
#     {
#         "road_surface": {
#             "black_concrete": 3,
#             "coal_block": 1,
#             "black_concrete_powder": 2,
#         },
#         "median_strip": {"stone": 1},
#         "structure": {"stone": 1},
#         "central_lines": {"yellow_concrete": 3, "yellow_concrete_powder": 1},
#         "external_lines": {"white_concrete": 3, "white_concrete_powder": 1},
#         "lines": {"white_concrete": 3, "white_concrete_powder": 1},
#         "road_under_top": {
#             "grass_block": 15,
#             "coarse_dirt": 3,
#             "podzol": 1,
#             "stone_slab": 2,
#         },
#         "road_top": {
#             "grass": 4,
#             "poppy": 1,
#             "dandelion": 1,
#             "fern": 3,
#             "tall_grass": 3,
#             "large_fern": 3,
#             "air": 8,
#         },
#     },
#     [
#         (51, 101, 31),
#         (4, 111, -60),
#         (88, 64, -128),
#     ],
#     90,
#     6,
#     factor=4,
# )

# intersection(
#     (0, 150, 0),
#     [
#         {
#             "coordinates": ((-10, 170, 30)),
#             "width": 2,
#             "blocks": {
#                 "road_surface": {
#                     "andesite": 3,
#                     "stone": 6,
#                     "cobblestone": 1,
#                 },
#                 "median_strip": {"stone": 1},
#             },
#         },
#         {
#             "coordinates": ((0, 170, -60)),
#             "width": 2,
#             "blocks": {
#                 "road_surface": {
#                     "andesite": 3,
#                     "stone": 6,
#                     "cobblestone": 1,
#                 },
#                 "median_strip": {"stone": 1},
#             },
#         },
#         {
#             "coordinates": ((-40, 170, -10)),
#             "width": 2,
#             "blocks": {
#                 "road_surface": {
#                     "andesite": 3,
#                     "stone": 6,
#                     "cobblestone": 1,
#                 },
#                 "median_strip": {"stone": 1},
#             },
#         },
#         {
#             "coordinates": ((30, 170, 10)),
#             "width": 2,
#             "blocks": {
#                 "road_surface": {
#                     "andesite": 3,
#                     "stone": 6,
#                     "cobblestone": 1,
#                 },
#                 "median_strip": {"stone": 1},
#             },
#         },
#     ],
# )