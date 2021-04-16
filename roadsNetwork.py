import numpy as np
import maths
import math
import main
import random


def roadIntersection(
    line0, line1, y=140
):  # HERE: Circle precision, USE_BATCHING, Circle SW not finish
    print("start")
    intersection = maths.lineIntersection(line0, line1)
    if intersection == None:
        return None

    angle = maths.getAngle(line0[0], intersection, line1[-1])
    StartDistance = 60 * abs(
        1 / (angle / 90)
    )  # Set here the radius of the circle for a square angle.

    startCurvePoint = maths.circle_line_segment_intersection(
        intersection, StartDistance, line0[0], intersection, full_line=True
    )[0]
    endCurvePoint = maths.circle_line_segment_intersection(
        intersection, StartDistance, line1[-1], intersection, full_line=True
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

    main.setCurveSurface("stone", np.array(points2), 5)

    # print(maths.getAngle(intersection, endCurvePoint, center))
    # print(maths.getAngle(intersection, startCurvePoint, center))


def highways(blocks, XZ, altitude, numberLanes, factor=4, destroy=False):
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
                        list(road_surface.keys()),
                        weights=road_surface.values(),
                        k=1,
                    )[0],
                    (xyz),
                )  # Surface road.
                main.setBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )  # Structure under the road.
                main.fillBlock(
                    "air",
                    (
                        xyz[0],
                        xyz[1] + 1,
                        xyz[2],
                        xyz[0],
                        xyz[1] + 3,
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


# roadIntersection(((70, 70), (100, 200)), ((150, 150), (50, 60)), y=140)
# roadIntersection(((-34, 78), (-52, 202)), ((28, 196), (-106, 143)),
# y=74)

highways(
    {
        "road_surface": {"andesite": 3, "stone": 6, "cobblestone": 1},
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
    },
    [(-130, 85, 168), (-77, 95, 93), (-80, 92, 0)],
    90,
    3,
    factor=4,
)
