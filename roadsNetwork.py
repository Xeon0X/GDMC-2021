import numpy as np
import maths
import math
import main


def roadIntersection(line0, line1):  # HERE
    intersection = maths.lineIntersection(line0, line1)
    if intersection == None:
        return None

    angle = maths.getAngle(line0[0], intersection, line1[-1])
    StartDistance = 40 + math.cos(angle) * 50  # Test value: 40.

    startCurvePoint = maths.circle_line_segment_intersection(
        intersection, StartDistance, line0[0], intersection, full_line=False
    )[0]
    endCurvePoint = maths.circle_line_segment_intersection(
        intersection, StartDistance, line1[-1], intersection, full_line=False
    )[0]
    print(startCurvePoint)

    perpendicular0 = maths.perpendicular(10, startCurvePoint, intersection)[0]
    perpendicular1 = maths.perpendicular(10, endCurvePoint, intersection)[0]
    print(perpendicular1)

    center = maths.lineIntersection(
        (perpendicular0, startCurvePoint), (perpendicular1, endCurvePoint)
    )

    main.setBlock("white_concrete", (center[0], 100, center[1]))
    main.setLine(
        "white_concrete",
        (line0[0][0], 105, line0[0][1]),
        (line0[1][0], 105, line0[1][1]),
    )
    main.setLine(
        "white_concrete",
        (line1[0][0], 105, line1[0][1]),
        (line1[1][0], 105, line1[1][1]),
    )


roadIntersection(((0, 0), (0, 100)), ((25, 25), (-25, 85)))
