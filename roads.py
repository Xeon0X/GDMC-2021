import numpy as np
import maths
import math
import main
import map
import schematic
import interfaceUtils as minecraft
import random

from PIL import Image
from collections import Counter

import csv

alreadyGenerated = []


######################## Lanes Materials Presets #######################


standard_modern_lane_composition = {
    "road_surface": {
        "black_concrete": 3,
        "coal_block": 1,
        "black_concrete_powder": 2,
    },
    "median_strip": {"stone": 1},
    "structure": {"stone": 3, "andesite": 1},
    "central_lines": {"yellow_concrete": 3, "yellow_concrete_powder": 1},
    "external_lines": {"white_concrete": 3, "white_concrete_powder": 1},
    "lines": {"white_concrete": 3, "white_concrete_powder": 1},
}


######################### Additional Functions #########################


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


def csvToList(csvFile, sep):
    """
    Parse and save values of a .csv into a list of list.

    Args:
        csv (.csv): The file.
        sep (str): The separator.
    """
    file = open(csvFile)
    table = csv.reader(file, delimiter=sep)
    table = list(table)
    file.close()
    return table


def strToInt(listOfLists):
    for list in range(len(listOfLists)):
        for element in range(len(listOfLists[list])):
            listOfLists[list][element] = int(listOfLists[list][element])
    return listOfLists


############################ Lanes Functions ###########################

housesCoordinates = []


def singleLaneLeft(XYZ, blocks=standard_modern_lane_composition):
    """Left side."""

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

    walkway = maths.curveSurface(
        np.array(XYZ),
        distance + 3,
        resolution=0,
        pixelPerfect=False,
        factor=4,
        start=3,
    )
    walkway = cleanLanes(walkway)

    houses = maths.curveSurface(
        np.array(XYZ),
        distance + 14,
        resolution=0,
        pixelPerfect=False,
        factor=1,
        start=distance + 13,
    )
    houses = cleanLanes(houses)

    road_surface = blocks.get("road_surface")
    structure = blocks.get("structure")

    for lane in roadSurface:
        for xyz in roadSurface[lane]:
            main.fillBlock(
                "air", (xyz[0], xyz[1], xyz[2], xyz[0], xyz[1] + 4, xyz[2])
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )
            main.setBlock(
                random.choices(
                    list(road_surface.keys()),
                    weights=road_surface.values(),
                    k=1,
                )[0],
                xyz,
            )
            alreadyGenerated.append((xyz[0], xyz[2]))

    lines = blocks.get("lines")
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == -1:
                main.setBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )
                main.setBlock(
                    random.choices(
                        list(lines.keys()),
                        weights=lines.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1], xyz[2]),
                )

    for lane in walkway:
        for xyz in walkway[lane]:
            if lane <= -1:
                counterSegments = 0
                main.fillBlock(
                    "air",
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] + 4, xyz[2]),
                )
                main.fillBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] - 1, xyz[2]),
                )
                alreadyGenerated.append((xyz[0], xyz[2]))

    counterSegments = 0
    for lane in houses:
        for xyz in houses[lane]:
            if lane <= -1:
                counterSegments += 1
                if counterSegments % 10 == 0:
                    housesCoordinates.append((xyz[0], xyz[1], xyz[2]))


def singleLaneRight(XYZ, blocks=standard_modern_lane_composition):
    """Right side."""

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

    walkway = maths.curveSurface(
        np.array(XYZ),
        distance + 3,
        resolution=0,
        pixelPerfect=False,
        factor=4,
        start=3,
    )
    walkway = cleanLanes(walkway)

    houses = maths.curveSurface(
        np.array(XYZ),
        distance + 14,
        resolution=0,
        pixelPerfect=False,
        factor=1,
        start=distance + 13,
    )
    houses = cleanLanes(houses)

    road_surface = blocks.get("road_surface")
    structure = blocks.get("structure")
    central_lines = blocks.get("central_lines")

    for lane in roadSurface:
        for xyz in roadSurface[lane]:
            main.fillBlock(
                "air", (xyz[0], xyz[1], xyz[2], xyz[0], xyz[1] + 4, xyz[2])
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )
            main.setBlock(
                random.choices(
                    list(road_surface.keys()),
                    weights=road_surface.values(),
                    k=1,
                )[0],
                xyz,
            )
            alreadyGenerated.append((xyz[0], xyz[2]))

    lines = blocks.get("lines")
    counterSegments = 0
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == 1:
                main.setBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )
                main.setBlock(
                    random.choices(
                        list(lines.keys()),
                        weights=lines.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1], xyz[2]),
                )

            if lane == -1:  # Central Lane.
                counterSegments += 1
                if counterSegments % 4 != 0:
                    main.setBlock(
                        random.choices(
                            list(structure.keys()),
                            weights=structure.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1] - 1, xyz[2]),
                    )
                    main.setBlock(
                        random.choices(
                            list(central_lines.keys()),
                            weights=central_lines.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )
                else:
                    main.setBlock(
                        random.choices(
                            list(structure.keys()),
                            weights=structure.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1] - 1, xyz[2]),
                    )
                    main.setBlock(
                        random.choices(
                            list(road_surface.keys()),
                            weights=road_surface.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )

    for lane in walkway:
        for xyz in walkway[lane]:
            if lane >= 1:
                main.fillBlock(
                    "air",
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] + 4, xyz[2]),
                )
                main.fillBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] - 1, xyz[2]),
                )
                alreadyGenerated.append((xyz[0], xyz[2]))

    counterSegments = 0
    for lane in houses:
        for xyz in houses[lane]:
            if lane >= 1:
                counterSegments += 1
                if counterSegments % 10 == 0:
                    housesCoordinates.append((xyz[0], xyz[1], xyz[2]))


def railway(XYZ, blocks=standard_modern_lane_composition):

    width = 9
    distance_from_edge = 7

    railway = maths.curveSurface(
        np.array(XYZ),
        width,
        resolution=0,
        pixelPerfect=False,
        factor=1,
        start=0,
        returnLine=False,
    )

    txt = open("coordinatesResult-1.txt", "w+")
    l = 0
    for lane in railway:
        if (lane == 0 or lane == -0) and l == 0:
            j = -1

            for xyz in railway[lane]:
                j += 1
                block = "stone"
                main.setBlock(
                    block,
                    xyz,
                )

                if j % 2 == 0:
                    pos = "//pos1"
                else:
                    pos = "//pos2"

                txt.write(
                    "/tp Xeon0X "
                    + str(xyz[0])
                    + " "
                    + str(xyz[1])
                    + " "
                    + str(xyz[2])
                    + "\n"
                    + pos
                    + "\n"
                    + str("")
                )

                if j >= 1:
                    txt.write("//line " + str("251:10") + "\n")
            l = 1
        else:
            l = 0

    txt.close()

    txt = open("coordinatesResult1.txt", "w+")
    for lane in railway:
        if lane == distance_from_edge or lane == -distance_from_edge:
            j = -1
            k = 0

            for xyz in railway[lane]:
                j += 1
                block = "red_wool"
                main.setBlock(
                    block,
                    xyz,
                )

                if j % 2 == 0:
                    pos = "//pos1"
                    line1 = xyz
                else:
                    pos = "//pos2"
                    line2 = xyz

                txt.write(
                    "/tp Xeon0X "
                    + str(xyz[0])
                    + " "
                    + str(xyz[1])
                    + " "
                    + str(xyz[2])
                    + "\n"
                    + pos
                    + "\n"
                )

                if j >= 1:
                    txt.write("//line " + str("251:14") + "\n")
                    # points = maths.line(line1, line2, pixelPerfect=True)
                    # for point in points:
                    #     k += 1
                    #     if k == 1:
                    #         main.setBlock(
                    #             "red_concrete",
                    #             point,
                    #         )
                    #         pos1 = point
                    #     if k == 2:
                    #         main.setBlock(
                    #             "orange_concrete",
                    #             point,
                    #         )
                    #     if k == 3:
                    #         main.setBlock(
                    #             "yellow_concrete",
                    #             point,
                    #         )
                    #     if k == 4:
                    #         k = 1
                    #         main.setLine(
                    #             "purple_concrete",
                    #             pos1,
                    #             point,
                    #             pixelPerfect=True,
                    #         )
                    #         #print(pos1, point)
                    #         #print(maths.perpendicular(3, pos1, point))
                    #         #pos1 = point

    txt.close()

    txt = open("coordinatesResult2.txt", "w+")
    for lane in railway:
        if lane == width - 1 or lane == -width + 1:
            j = -1

            for xyz in railway[lane]:
                j += 1
                block = "pink_wool"
                main.setBlock(
                    block,
                    xyz,
                )

                if j % 2 == 0:
                    pos = "//pos1"
                else:
                    pos = "//pos2"

                txt.write(
                    "/tp Xeon0X "
                    + str(xyz[0])
                    + " "
                    + str(xyz[1])
                    + " "
                    + str(xyz[2])
                    + "\n"
                    + pos
                    + "\n"
                )

                if j >= 1:
                    txt.write("//line " + str("251:11") + "\n")

    txt.close()

    # 2
    # for lane in railway:
    #     for i in range(1, len(railway[lane])):
    #         print(railway)

    #         xy = maths.perpendicular(
    #             5,
    #             (railway[lane][i][0], railway[lane][i][2]),
    #             (railway[lane][i - 1][0], railway[lane][i - 1][2]),
    #         )
    #         main.setBlock(
    #             "light_blue_wool",
    #             (xy[0][0], railway[lane][i][1], xy[0][1]),
    #         )
    #         main.setBlock(
    #             "pink_wool", (xy[1][0], railway[lane][i][1], xy[1][1])
    #         )

    # 1
    # line = []
    # for lane in railway:
    #     for i in range(1, len(railway[lane])):
    #         line.extend(maths.line(railway[lane][i - 1], railway[lane][i]))

    # for i in range(2, len(line)):
    #     print(i, i % 3)
    #     if i % 3 == 0:
    #         print("eee")
    #         xy = maths.perpendicular(
    #             5,
    #             (line[i][0], line[i][2]),
    #             (line[i - 1][0], line[i - 1][2]),
    #         )
    #         main.setBlock("blue_wool", (xy[0][0], line[i][1], xy[0][1]))
    #         main.setBlock("red_wool", (xy[1][0], line[i][1], xy[1][1]))


############################ Roads Generator ###########################


class RoadCurve:
    def __init__(self, roadData, XYZ):
        print("road, first input:", XYZ)
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

        singleLaneRight(
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
        -1: {"type": singleLaneLeft, "centerDistance": -3},
        1: {"type": singleLaneRight, "centerDistance": 3},
    },
}


railway_agencement = {
    "lanes": {
        1: {"type": railway, "centerDistance": 0},
    },
}


standard_modern_lanes_agencement = {
    "mainRoads": {
        0: {
            "lanes": {
                -1: {"type": singleLaneLeft, "centerDistance": -5},
                0: {"type": singleLaneLeft, "centerDistance": 0},
                1: {"type": singleLaneRight, "centerDistance": 5},
            }
        },
        1: {
            "lanes": {
                -1: {"type": singleLaneRight, "centerDistance": -5},
                0: {"type": singleLaneRight, "centerDistance": 0},
                1: {"type": singleLaneRight, "centerDistance": 5},
            }
        },
    },
    "sideRoads": {
        0: {
            "lanes": {
                -1: {"type": singleLaneLeft, "centerDistance": -5},
                1: {"type": singleLaneLeft, "centerDistance": 0},
                2: {"type": singleLaneLeft, "centerDistance": 5},
            }
        },
        1: {
            "lanes": {
                -1: {"type": singleLaneLeft, "centerDistance": -5},
                1: {"type": singleLaneLeft, "centerDistance": 0},
                2: {"type": singleLaneLeft, "centerDistance": 5},
            }
        },
    },
}

autoMode = 0
if __name__ == "__main__":
    if autoMode == 1:
        debug = False

        # Find the area.
        area = minecraft.requestBuildArea()
        area = map.areaCoordinates(
            (area["xFrom"], area["zFrom"]), (area["xTo"], area["zTo"])
        )
        print("area:", area)

        # Generate data to work with.
        map.heightmap(
            area[0],
            area[1],
            mapName="heightmap.png",
            biomeName="heightmap_biome.png",
        )
        map.blur("heightmap_biome.png", name="heightmap_biome.png", factor=11)
        map.sobel("heightmap.png")
        map.blur(
            "heightmap_biome.png", name="heightmap_medianBlur.png", factor=11
        )
        (
            pixel_graph_row,
            pixel_graph_col,
            pixel_graph_data,
            coordinates,
        ) = map.skel("heightmap_medianBlur.png", "heightmap_skeletonize.png")
        lines, intersections, center = map.parseGraph(
            pixel_graph_row, pixel_graph_col
        )

        if debug:
            print(center)
            print(lines)
            print(intersections)

        # Colorization

        # Lines
        path = "heightmap_skeletonize_color.png"
        im = Image.open("heightmap_skeletonize.png")
        width, height = im.size
        # img = Image.new(mode="RGB", size=(width, height))
        img = Image.open("heightmap_sobel.png")
        for i in range(len(lines)):
            r, g, b = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for j in range(len(lines[i])):
                img.putpixel(
                    (
                        int(coordinates[lines[i][j]][0]),
                        int(coordinates[lines[i][j]][1]),
                    ),
                    (r + j, g + j, b + j),
                )
        img.save(path, "PNG")

        # Centers
        img = Image.open(path)
        for i in range(len(center)):
            if debug:
                print(coordinates[center[i]])
            img.putpixel(
                (
                    int(coordinates[center[i]][0]),
                    int(coordinates[center[i]][1]),
                ),
                (255, 255, 0),
            )
        img.save(path, "PNG")

        # Intersections
        for i in range(len(intersections)):
            intersection = []
            for j in range(len(intersections[i])):
                intersection.append(coordinates[intersections[i][j]])
            if debug:
                print(intersection)

            img = Image.open(path)
            for i in range(len(intersection)):
                img.putpixel(
                    (int(intersection[i][0]), int(intersection[i][1])),
                    (255, 0, 255),
                )
            img.save(path, "PNG")

        # Generation
        for i in range(len(lines)):
            for j in range(len(lines[i])):
                xz = map.irlToMc(area[0], coordinates[lines[i][j]])
                lines[i][j] = xz

        # Simplification
        from simplification.cutil import simplify_coords

        for i in range(len(lines)):
            if debug:
                print(lines[i])
            lines[i] = simplify_coords(lines[i], 1.0)

        for i in range(len(lines)):
            for j in range(len(lines[i])):
                xyz = map.findGround(area[0], lines[i][j])
                lines[i][j] = xyz

        for i in range(
            len(lines)
        ):  # HERE --------------------------------------
            road = RoadCurve(standard_modern_lane_agencement, lines[i])
            road.setLanes()
            # print(road.getLanes(), "LANES ***********")

        # i = 5
        # road = RoadCurve(standard_modern_lane_agencement, lines[i])
        # road.setLanes()
        rejected = []
        accepted = []
        # print(housesCoordinates)
        for i in range(len(housesCoordinates)):
            pos = housesCoordinates[i]
            # print(pos, "pos0")
            base = map.findGround(area[0], pos)
            if base != None:
                # print(pos, "pos1")
                pos1 = (
                    pos[0] - random.randint(6, 19),
                    base[1],
                    pos[2] - random.randint(6, 19),
                )
                pos2 = (
                    pos[0] + random.randint(6, 19),
                    base[1],
                    pos[2] + random.randint(6, 19),
                )
                # pos3 = (
                #     pos1[0],
                #     base[1],
                #     pos2[2],
                # )
                # pos4 = (
                #     pos2[0],
                #     base[1],
                #     pos1[2],
                # )

                pos3 = (
                    pos[0] + random.randint(3, 9),
                    base[1],
                    pos[2] - random.randint(3, 9),
                )

                pos4 = (
                    pos[0] - random.randint(3, 9),
                    base[1],
                    pos[2] + random.randint(3, 9),
                )

                # print(pos1, pos2, pos3, pos4, "pos")
                Ypos1 = map.findGround(area[0], pos1)
                Ypos2 = map.findGround(area[0], pos2)
                Ypos3 = map.findGround(area[0], pos3)
                Ypos4 = map.findGround(area[0], pos4)

                if (
                    Ypos1 != None
                    and Ypos2 != None
                    and Ypos3 != None
                    and Ypos4 != None
                ):

                    pos2 = (
                        pos2[0],
                        max(Ypos1[1], Ypos2[1], base[1], Ypos3[1], Ypos4[1]),
                        pos2[2],
                    )
                    pos1 = (
                        pos1[0],
                        max(Ypos1[1], Ypos2[1], base[1], Ypos3[1], Ypos4[1]),
                        pos1[2],
                    )
                    if (
                        (pos1[0], pos1[2]) not in alreadyGenerated
                        and (
                            pos2[0],
                            pos2[2],
                        )
                        not in alreadyGenerated
                        and (pos1[0], pos2[2]) not in alreadyGenerated
                        and (pos2[0], pos1[2])
                    ):  # HERE, remove print and find why house gen on self

                        for xi in range(
                            -5,
                            (max(pos1[0], pos2[0]) - min(pos1[0], pos2[0]))
                            + 5,
                        ):
                            for yi in range(
                                -5,
                                (max(pos1[2], pos2[2]) - min(pos1[2], pos2[2]))
                                + 5,
                            ):
                                alreadyGenerated.append(
                                    (
                                        min(pos1[0], pos2[0]) + xi,
                                        min(pos1[2], pos2[2]) + yi,
                                    )
                                )

                        door = ["south", "north", "east", "west"]
                        cb = random.randint(0, 3)
                        # schematic.house(
                        #     pos1,
                        #     pos2,
                        #     door[cb],
                        #     random.randint(0, 1),
                        #     min(
                        #         Ypos1[1], Ypos2[1], base[1], Ypos3[1], Ypos4[1]
                        #     ),
                        # )

                        import builds

                        builds.middleResidentialTower(
                            (
                                (pos1[0], pos1[2]),
                                (pos3[0], pos3[2]),
                                (pos2[0], pos2[2]),
                                (pos4[0], pos4[2]),
                            ),
                            (),
                            (
                                int(Ypos1[1]),
                                (
                                    int(Ypos1[1])
                                    + random.randint(20, (255 - int(Ypos1[1])))
                                ),
                            ),
                        )

                        accepted.append(
                            (
                                pos1[0],
                                pos1[2],
                                pos2[0],
                                pos2[2],
                            )
                        )
                    else:
                        rejected.append(
                            (
                                pos1[0],
                                pos1[2],
                                pos2[0],
                                pos2[2],
                            )
                        )

    if autoMode == 0:
        coordinates = strToInt(csvToList("coordinates.csv", ";"))
        road = RoadCurve(railway_agencement, coordinates)
        road.setLanes()
        result = road.getLanes()

        txt = open("coordinatesResultMid.txt", "w+")

        for __, i in enumerate(result):
            for j in range(len(result[i])):
                coordinate = ""
                coordinate += (
                    str(result[i][j][0])
                    + " "
                    + str(int(result[i][j][1]) + 1)
                    + " "
                    + str(result[i][j][2])
                )
                if j % 2 == 0:
                    pos = "//pos1"
                else:
                    pos = "//pos2"

                txt.write("/tp Xeon0X " + str(coordinate) + "\n" + pos + "\n")

                if j >= 1:
                    txt.write("//line " + str(1) + "\n")

        txt.close()

    print("Done")