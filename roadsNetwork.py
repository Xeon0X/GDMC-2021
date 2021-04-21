import numpy as np
import maths
import math
import main
import random


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


def intersection(centerPoint, roadsData):
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

    # Find the intersection for all the roads.
    intersections = []
    for i in range(0, len(roads), 2):
        line0 = roads[i]
        line1 = roads[i - 1]
        main.setLine("white_concrete", line0[0], line0[1])
        main.setLine("red_concrete", line1[0], line1[1])
        intersectionPoints = maths.curveCornerIntersection(line0, line1, 10)
        if intersection != None:
            for i in range(len(intersectionPoints)):
                main.setBlock(
                    "white_concrete",
                    (
                        round(intersectionPoints[i][0]),
                        165,
                        round(intersectionPoints[i][1]),
                    ),
                )


# roadIntersection(((70, 70), (100, 200)), ((150, 150), (50, 60)), y=140)
# roadIntersection(((-34, 78), (-52, 202)), ((28, 196), (-106, 143)),
# y=74)

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
#         (39, 75, 90),
#         (-15, 76, 133),
#         (-20, 90, 198),
#     ],
#     90,
#     2,
#     factor=4,
# )

intersection(
    (0, 150, 0),
    [
        {
            "coordinates": ((-10, 150, 30)),
            "width": 7,
            "blocks": {
                "road_surface": {
                    "andesite": 3,
                    "stone": 6,
                    "cobblestone": 1,
                },
                "median_strip": {"stone": 1},
            },
        },
        {
            "coordinates": ((0, 150, -60)),
            "width": 5,
            "blocks": {
                "road_surface": {
                    "andesite": 3,
                    "stone": 6,
                    "cobblestone": 1,
                },
                "median_strip": {"stone": 1},
            },
        },
        {
            "coordinates": ((-40, 150, -10)),
            "width": 10,
            "blocks": {
                "road_surface": {
                    "andesite": 3,
                    "stone": 6,
                    "cobblestone": 1,
                },
                "median_strip": {"stone": 1},
            },
        },
        {
            "coordinates": ((30, 150, 10)),
            "width": 7,
            "blocks": {
                "road_surface": {
                    "andesite": 3,
                    "stone": 6,
                    "cobblestone": 1,
                },
                "median_strip": {"stone": 1},
            },
        },
    ],
)

# print(
#     maths.lineIntersection(
#         ((-3, 100, 93), (27, 100, 123)),
#         ((24, 100, 108), (14, 100, 116)),
#         segments=True,
#     )
# )