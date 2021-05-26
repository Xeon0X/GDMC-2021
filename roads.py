import numpy as np
import maths
import math
import main
import random


######################## Lanes materials presets #######################


standard_modern_lane_composition = {
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
}


######################### Additional functions #########################


def cleanLanes(lanes):
    cleanLanes = {}
    for lane in lanes:
        for xyz in lanes[lane]:
            if (round(xyz[0]), round(xyz[1]), round(xyz[2]),) not in [
                cleanLanes[i][j]
                for __, i in enumerate(cleanLanes)
                for j in range(len(cleanLanes[i]))
            ]:
                if cleanLanes.get(lane) == None:
                    cleanLanes[lane] = []
                cleanLanes[lane].append(
                    (round(xyz[0]), round(xyz[1]), round(xyz[2]))
                )
    return cleanLanes


############################ Lanes functions ###########################


def singleLane(XYZ, blocks=standard_modern_lane_composition):
    """Generate a single and simple modern lane."""

    factor = 8
    distance = 2

    roadMarkings = maths.curveSurface(
        np.array(XYZ),
        distance + 1,
        resolution=0,
        pixelPerfect=True,
        factor=1,
        start=2,
    )
    roadMarkings = cleanLanes(roadMarkings)

    roadSurface = maths.curveSurface(
        np.array(XYZ),
        distance,
        resolution=0,
        pixelPerfect=False,
        factor=factor,
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
                xyz,
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )

    lines = blocks.get("lines")
    counterSegments = 0
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == -1 or lane == 1:
                counterSegments += 1
                if counterSegments % 4 != 0:
                    main.setBlock(
                        random.choices(
                            list(lines.keys()),
                            weights=lines.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )


def singleLane2(XYZ, blocks=standard_modern_lane_composition):
    """Generate a single and simple modern lane."""

    factor = 8
    distance = 2

    roadMarkings = maths.curveSurface(
        np.array(XYZ),
        distance + 1,
        resolution=0,
        pixelPerfect=True,
        factor=1,
        start=2,
    )
    roadMarkings = cleanLanes(roadMarkings)

    roadSurface = maths.curveSurface(
        np.array(XYZ),
        distance,
        resolution=0,
        pixelPerfect=False,
        factor=factor,
    )
    roadSurface = cleanLanes(roadSurface)

    road_surface = {
        "stone": 3,
        "andesite": 1,
    }
    structure = blocks.get("structure")
    for lane in roadSurface:
        for xyz in roadSurface[lane]:
            main.setBlock(
                random.choices(
                    list(road_surface.keys()),
                    weights=road_surface.values(),
                    k=1,
                )[0],
                xyz,
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )

    lines = blocks.get("lines")
    counterSegments = 0
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == -1 or lane == 1:
                counterSegments += 1
                if counterSegments % 4 != 0:
                    main.setBlock(
                        random.choices(
                            list(lines.keys()),
                            weights=lines.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )


############################ Roads Generator ###########################


class RoadCurve:
    def __init__(self, roadData, XYZ):
        print("road:", XYZ)
        """Create points that forms the lanes depending of the roadData."""
        self.roadData = roadData
        self.XYZ = XYZ

        # Find the offset, where the lanes is.
        self.lanesXYZ = {}
        for __, i in enumerate(self.roadData["lanes"]):
            laneCenterDistance = self.roadData["lanes"][i]["centerDistance"]
            self.lanesXYZ[i] = maths.curveSurface(
                np.array(XYZ),
                abs(laneCenterDistance),
                resolution=0,
                pixelPerfect=True,
                factor=1,
                start=abs(laneCenterDistance) - 1,
                returnLine=False,
            )
            # We only take the desired side.
            if laneCenterDistance == 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][0]
            if laneCenterDistance > 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][1]
            if laneCenterDistance < 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][-1]

    def setLanes(self, lanes=[]):
        """Generate the lanes depending of the function name."""
        for __, i in enumerate(self.roadData["lanes"]):
            if i in lanes or lanes == []:
                self.roadData["lanes"][i]["type"](np.array(self.lanesXYZ[i]))

    def getLanes(self, lanes=[]):
        """Return the points that forms the lanes."""
        lanesDict = {}
        for __, i in enumerate(self.roadData["lanes"]):
            if i in lanes or lanes == []:
                lanesDict[i] = self.lanesXYZ[i]
        return lanesDict


def DELETEintersection(roadsData, centerPoint, mainRoads, sideRoads):
    """
    [summary]

    [extended_summary]

    Args:
        roadsData (dict): standard_modern_lanes_agencement
        centerPoint (tuple): (x, y, z)
        mainRoads (list): {0:((x, y, z), (x, y, z)), 1:((x, y, z), (x, y, z))}
        sideRoads ([type]): {0:[(x, y, z), 1:(x, y, z), -1:(x, y, z), 2:(x, y, z)}
    """
    # Save all the lanes.
    lanes = {}

    # Set the side roads.
    for i in roadsData["sideRoads"]:
        sideRoad = RoadCurve(
            roadsData["sideRoads"].get(i), (sideRoads.get(i), centerPoint)
        )
        sideRoad.setLanes()
        lanes[sideRoads[i]] = sideRoad.getLanes()

    # Set the main roads.
    for i in roadsData["mainRoads"]:
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i), (mainRoads.get(i)[0], centerPoint)
        )
        mainRoad.setLanes()
        lanes[mainRoads[i][0]] = mainRoad.getLanes()
        # We don't want to inverse the orientation of the main road.
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i), (centerPoint, mainRoads.get(i)[1])
        )
        mainRoad.setLanes()
        # But we want to save it like the others.
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i),
            (
                mainRoads.get(i)[1],
                centerPoint,
            ),
        )
        lanes[mainRoads[i][1]] = mainRoad.getLanes()

    # Sort all the points in rotation order.
    points = []
    points.extend([xyz[i] for xyz in mainRoads.values() for i in range(2)])
    points.extend([xyz for xyz in sideRoads.values()])
    points = maths.sortRotation(points)

    # Compute the curve between each road.
    y = 150
    for i in range(len(points)):

        a = random.randint(0, 6)
        if a == 0:
            b = "blue_concrete"
        elif a == 1:
            b = "red_concrete"
        elif a == 2:
            b = "green_concrete"
        elif a == 3:
            b = "yellow_concrete"
        elif a == 4:
            b = "pink_concrete"
        elif a == 5:
            b = "orange_concrete"
        else:
            b = "brown_concrete"

        line0 = (
            lanes[points[i]][max(lanes[points[i]])][0],
            lanes[points[i]][max(lanes[points[i]])][1],
        )
        line1 = (
            lanes[points[i - 1]][min(lanes[points[-1]])][0],
            lanes[points[i - 1]][min(lanes[points[-1]])][1],
        )

        # Compute the curve.
        intersectionPointsTemp = maths.curveCornerIntersectionPoints(
            line0, line1, 10, angleAdaptation=False
        )

        # Complete the points of the curve with a few points of the line
        # to stabilize the curve.
        intersectionPoints = [(line0[0])]
        [
            intersectionPoints.append((round(xz[0]), y, round(xz[1])))
            for xz in intersectionPointsTemp
            if (round(xz[0]), y, round(xz[1])) not in intersectionPoints
        ]
        intersectionPoints.insert(
            1, maths.middleLine(intersectionPoints[1], intersectionPoints[0])
        )
        intersectionPoints.insert(
            2, maths.middleLine(intersectionPoints[1], intersectionPoints[2])
        )
        intersectionPoints.append((line1[0]))
        # intersectionPoints.insert(
        #     -1,
        #     maths.middleLine(intersectionPoints[-2], intersectionPoints[-1]),
        # )
        # intersectionPoints.insert(
        #     -2,
        #     maths.middleLine(intersectionPoints[-2], intersectionPoints[-3]),
        # )

        # Generate the curve.
        for key, value in lanes.items():
            for __, value1 in value.items():
                if intersectionPoints[0] in value1:
                    # Key found.
                    for __, j in enumerate(mainRoads):
                        if key in mainRoads[j]:
                            curveRoad = RoadCurve(
                                roadsData["mainRoads"][j], intersectionPoints
                            )
                            curveRoad.setLanes(
                                [max(roadsData["mainRoads"][j]["lanes"])]
                            )
                    # for __, j in enumerate(sideRoads):
                    #     print(sideRoads[j])
                    #     if key == sideRoads[j]:
                    #         print(
                    #             roadsData["sideRoads"][j], intersectionPoints
                    #         )
                    #         curveRoad = Road(
                    #             roadsData["sideRoads"][j], intersectionPoints
                    #         )
                    #         curveRoad.setLanes(
                    #             [min(roadsData["sideRoads"][j]["lanes"])]
                    #         )


def intersection(
    roadsData, centerPoint, mainRoads, sideRoads
):  # TODO: Refactoring. Error with y in curve.
    """
    [summary]

    [extended_summary]

    Args:
        roadsData (dict): standard_modern_lanes_agencement
        centerPoint (tuple): (x, y, z)
        mainRoads (list): {0:((x, y, z), (x, y, z)), 1:((x, y, z), (x, y, z))}
        sideRoads ([type]): {0:[(x, y, z), 1:(x, y, z), -1:(x, y, z), 2:(x, y, z)}
    """
    # Save all the lanes.
    lanes = {}

    # Set the side roads.
    for i in roadsData["sideRoads"]:
        sideRoad = RoadCurve(
            roadsData["sideRoads"].get(i), (sideRoads.get(i), centerPoint)
        )
        sideRoad.setLanes()
        lanes[sideRoads[i]] = sideRoad.getLanes()

    # Set the main roads.
    for i in roadsData["mainRoads"]:
        mainLanes = []
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i), (mainRoads.get(i)[0], centerPoint)
        )
        mainRoad.setLanes()
        lanes[mainRoads[i][0]] = mainRoad.getLanes()
        mainLanes.append(mainRoad.getLanes())
        # We don't want to inverse the orientation of the main road.
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i), (centerPoint, mainRoads.get(i)[1])
        )
        mainRoad.setLanes()
        # But we want to save it like the others.
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i),
            (
                mainRoads.get(i)[1],
                centerPoint,
            ),
        )
        lanes[mainRoads[i][1]] = mainRoad.getLanes()
        mainLanes.append(mainRoad.getLanes())

        # # Compute the curve of the main road.
        # center = ()
        # for j in list(mainRoad.getLanes().keys()):

        #     line0 = (mainLanes[0][j][0], mainLanes[0][j][1])
        #     line1 = (mainLanes[1][j][0], mainLanes[1][j][1])

        #     intersectionPointsTemp, center = maths.curveCornerIntersectionLine(
        #         line0, line1, 70, angleAdaptation=False, center=center
        #     )

        #     y = 205
        #     intersectionPoints = []
        #     [
        #         intersectionPoints.append((round(xz[0]), y, round(xz[1])))
        #         for xz in intersectionPointsTemp
        #         if (round(xz[0]), y, round(xz[1])) not in intersectionPoints
        #     ]
        #     print(intersectionPointsTemp, center)

        #     singleLane2(
        #         intersectionPoints, blocks=standard_modern_lane_composition
        #     )

    # Sort all the points in rotation order.
    points = []
    points.extend([xyz[i] for xyz in mainRoads.values() for i in range(2)])
    points.extend([xyz for xyz in sideRoads.values()])
    points = maths.sortRotation(points)

    # Compute the curve between each road.
    for i in range(len(points)):
        line0 = (
            lanes[points[i]][max(lanes[points[i]])][0],
            lanes[points[i]][max(lanes[points[i]])][1],
        )
        line1 = (
            lanes[points[i - 1]][min(lanes[points[-1]])][0],
            lanes[points[i - 1]][min(lanes[points[-1]])][1],
        )

        # Compute the curve.
        intersectionPointsTemp = maths.curveCornerIntersectionLine(
            line0, line1, 10, angleAdaptation=False
        )[0]

        y = centerPoint[1]  # Not the real y here
        intersectionPoints = []
        [
            intersectionPoints.append((round(xz[0]), y, round(xz[1])))
            for xz in intersectionPointsTemp
            if (round(xz[0]), y, round(xz[1])) not in intersectionPoints
        ]
        diffAlt = abs(line0[0][1] - line1[0][1])
        maxAlt = max(line0[0][1], line1[0][1])
        print(diffAlt, maxAlt, len(intersectionPoints))
        if diffAlt != 0:
            step = len(intersectionPoints) // diffAlt
        else:
            step = 1
        for i in range(len(intersectionPoints)):
            print(i)
            intersectionPoints[i] = (
                intersectionPoints[i][0],
                maxAlt - (i // step),
                intersectionPoints[i][2],
            )

        singleLane2(
            intersectionPoints, blocks=standard_modern_lane_composition
        )

        # # Generate the curve.
        # for key, value in lanes.items():
        #     for __, value1 in value.items():
        #         if intersectionPoints[0] in value1:
        #             # Key found.
        #             for __, j in enumerate(mainRoads):
        #                 if key in mainRoads[j]:
        #                     curveRoad = RoadCurve(
        #                         roadsData["mainRoads"][j], intersectionPoints
        #                     )
        #                     curveRoad.setLanes(
        #                         [max(roadsData["mainRoads"][j]["lanes"])]
        #                     )
        #             # for __, j in enumerate(sideRoads):
        #             #     print(sideRoads[j])
        #             #     if key == sideRoads[j]:
        #             #         print(
        #             #             roadsData["sideRoads"][j], intersectionPoints
        #             #         )
        #             #         curveRoad = Road(
        #             #             roadsData["sideRoads"][j], intersectionPoints
        #             #         )
        #             #         curveRoad.setLanes(
        #             #             [min(roadsData["sideRoads"][j]["lanes"])]
        #             #         )


############################# Lanes Preset #############################


standard_modern_lane_agencement = {
    "lanes": {
        -1: {"type": singleLane, "centerDistance": -3},
        1: {"type": singleLane, "centerDistance": 3},
        2: {"type": singleLane, "centerDistance": 6},
    },
}


standard_modern_lanes_agencement = {
    "mainRoads": {
        0: {
            "lanes": {
                -1: {"type": singleLane, "centerDistance": -5},
                0: {"type": singleLane, "centerDistance": 0},
                1: {"type": singleLane2, "centerDistance": 5},
            }
        },
        1: {
            "lanes": {
                -1: {"type": singleLane2, "centerDistance": -5},
                0: {"type": singleLane2, "centerDistance": 0},
                1: {"type": singleLane2, "centerDistance": 5},
            }
        },
    },
    "sideRoads": {
        0: {
            "lanes": {
                -1: {"type": singleLane, "centerDistance": -5},
                1: {"type": singleLane, "centerDistance": 0},
                2: {"type": singleLane, "centerDistance": 5},
            }
        },
        1: {
            "lanes": {
                -1: {"type": singleLane, "centerDistance": -5},
                1: {"type": singleLane, "centerDistance": 0},
                2: {"type": singleLane, "centerDistance": 5},
            }
        },
    },
}


# intersection(
#     standard_modern_lanes_agencement,
#     (150, 140, -150),
#     {
#         0: ((200, 140, -80), (100, 140, -115)),
#         1: ((120, 140, -80), (200, 140, -150)),
#     },
#     {0: (50, 140, -200), 1: (150, 140, -200), 2: (175, 140, -175)},
# )

# intersection(
#     standard_modern_lanes_agencement,
#     (300, 130, 100),
#     {
#         0: ((300, 130, 0), (300, 130, 200)),
#         1: ((250, 130, 150), (350, 130, -50)),
#     },
#     {0: (400, 130, 200), 1: (250, 130, 50)},
# )


# roadTest = Road(
#     standard_modern_lane_agencement,
#     (
#         (70, 70 + 15, -20),
#         (160, 68 + 15, -128),
#         (235, 64 + 15, -215),
#     ),
# )

# roadTest.setLanes()