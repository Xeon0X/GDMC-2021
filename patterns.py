import maths
import main
import random


######################### Additional Functions #########################


def combineLines(XYZ, pixelPerfect=True):
    """
    Combine several lines to obtain a continuous set of points.

    TODO:
        cleanLine

    Args:
        XYZ (List of tuples): All the points that forms the line.
        pixelPerfect (bool, optional): Defaults to True.

    Returns:
        list: A continuous set of points coordinates.
    """
    lines = []
    for i in range(len(XYZ) - 1):
        line = maths.line(XYZ[i], XYZ[i + 1], pixelPerfect)
        lines.extend(line)  # To be cleaned
    return lines


def randomBlock(blocks):
    """
    Chose a random block.

    Args:
        blocks (dict): See example input.

    Returns:
        str: The chosen block.

    Example input:
        blocks = {
            "light_gray_stained_glass": 2,
            "black_stained_glass_pane": 1,
        }
    """
    return random.choices(
        list(blocks.keys()),
        weights=blocks.values(),
        k=1,
    )[0]


def getOrientation(orientation):
    if orientation == "north":
        return 0, -1  # x, z
    if orientation == "south":
        return 0, 1  # x, z
    if orientation == "east":
        return 1, 0  # x, z
    if orientation == "west":
        return -1, 0  # x, z


def dict_to_list(d):
    l = []
    for key in d:
        for i in range(d[key]):
            l.append(key)
    return l


def add_to_tuple(tuple_list, x, y, z):
    new_list = []
    for i in tuple_list:
        new_list.append((i[0] + x, i[1] + y, i[2] + z))
    return new_list


########################## Materials Presets ###########################
"""
Dictionary that defines the blocks that can be used to generate the
façade.
"""


########################## Arguments Presets ###########################


simpleWindowPattern1 = {
    "windowSize": (2, 3),
    "windowSpacingSide": 1,
    "windowSpacingTopBot": 1,
}

# A list for different values depending on the floor? No, stage height
# are equal, because to complicated. Instead, divide the pattern
# vertically, with different settings.
# towerBalconyPreset = {
#     "height_ceiling": 4,
#     "floors_spacing": 0,
#     "balcony": {
#         "type": floorNoConnectedTexture,
#         "height": 1,
#         "width": 4,
#         "blocks": {
#             "ground": {"andesite": 1},  # Specific here.
#             "separator": {"stone_brick_stairs": 1},  # Specific here.
#         },
#     },
#     "exterior_wall": {
#         "type": bayWindow,
#         "height": 4,
#         "width": 1,
#         "blocks": {
#             "light_gray_stained_glass": 2,
#             "black_stained_glass_pane": 1,
#         },
#     },
#     "railing": {
#         "type": concrete,
#         "height": 2,
#         "width": 1,
#         "blocks": {
#             "red_concrete": 1,
#             "red_terracotta": 2,
#             "pink_terracotta": 1,
#         },
#     },
#     "pillars": {
#         "type": simplePillar,
#         "height": 4,
#         "spacing": [5],  # To make irregular pattern. Horizontally.
#         "blocks": {"blackstone_wall": 1},
#     },
# }


########################### Builder Functions ##########################


def randomPattern(XYZ, height, width, orientation, randomType, blocks):
    line = combineLines(XYZ, pixelPerfect=True)

    x, z = getOrientation(orientation)

    if randomType == "all":
        for y in range(height):
            for i in range(len(line)):
                for j in range(width):
                    main.setBlock(
                        randomBlock(blocks),
                        (
                            line[i][0] + x * j,
                            line[i][1] + y,
                            line[i][2] + z * j,
                        ),
                    )

    if randomType == "vertical":
        for y in range(height):
            block = randomBlock(blocks)
            for i in range(len(line)):
                for j in range(width):
                    main.setBlock(
                        block,
                        (
                            line[i][0] + x * j,
                            line[i][1] + y,
                            line[i][2] + z * j,
                        ),
                    )

    if randomType == "horizontal":
        for i in range(len(line)):
            block = randomBlock(blocks)
            for y in range(height):
                for j in range(width):
                    main.setBlock(
                        block,
                        (
                            line[i][0] + x * j,
                            line[i][1] + y,
                            line[i][2] + z * j,
                        ),
                    )


def regularPattern(XYZ, height, width, orientation, patternType, blocks):
    line = combineLines(XYZ, pixelPerfect=True)
    pattern = dict_to_list(blocks)
    # Here the values are used as the number of times the block appears.

    x, z = getOrientation(orientation)
    yC = 0

    if patternType == "vertical":
        for y in range(height):
            block = pattern[yC]
            yC += 1
            if yC >= len(pattern):
                yC = 0

            for i in range(len(line)):
                for j in range(width):
                    main.setBlock(
                        block,
                        (
                            line[i][0] + x * j,
                            line[i][1] + y,
                            line[i][2] + z * j,
                        ),
                    )

    if patternType == "horizontal":
        for i in range(len(line)):
            block = pattern[yC]
            yC += 1
            if yC >= len(pattern):
                yC = 0

            for y in range(height):
                for j in range(width):
                    main.setBlock(
                        block,
                        (
                            line[i][0] + x * j,
                            line[i][1] + y,
                            line[i][2] + z * j,
                        ),
                    )


########################## Assembler Functions #########################
"""
Object?

Initialization: Take coordinates, compute the distance.
getNumberWindows: Based on the distance, estimate the number of possible
windows with this setting.
getSettingsWindows: Find the possible settings windows to place n number
of windows.
addVerticalLine
addHorizontalLine

getRelief: Compute the relief based on the blocks used and their
placement. Find good and bad values.
getComplexity: Compute the complexity based on the blocks used. Find
good and bad values.

setPattern: place the pattern.
"""

"""
Universal class for roads and patterns?
"""

"""
Patterns should be able to be generated in diagonals, rotating around
the Y axis, and also on different ground levels.

Patterns can be modular, meaning that inside the pattern there will be
parts that can be expanded (like windows, or space between windows, in 2
dimensions).

Patterns should support palettes blocks.

Patterns can take more than two coordinates as inputs, to be defined on
a curve for example.

Patterns are repeated in one direction only. Sure?
"""


def simpleWindowPattern(XYZ, height, args, blocks=None):
    """
    Generate a simple window pattern.

    Args:
        XYZ (list): List of tuple, the xyz coordinates.
        args (dict): All the arguments, specific to this pattern.
        blocks (dict): Blocks palette, defined in Materials Presets.

    Example:
        simpleWindowPattern([(x, y, z), (x, y, z), (x, y, z)],
        {"windowSize": (xSize, zSize), "windowSpace": (botSpace, topSpace,
        betweenSpace)}, {"structure": {[...]}, "glass":{[...]}})
    """
    lines = []
    for i in range(len(XYZ) - 1):
        line = maths.line(XYZ[i], XYZ[i + 1], pixelPerfect=True)
        lines.extend(line)  # To be cleaned

    windowArea = [
        (args["windowSpacingSide"], args["windowSpacingTopBot"]),
        (
            args["windowSpacingSide"] + args["windowSize"][0],
            args["windowSpacingTopBot"] + args["windowSize"][1],
        ),
    ]
    xPattern = -1
    yPattern = -1
    print(lines)
    for x in range(len(lines)):
        xPattern += 1
        if xPattern >= (
            2 * int(args["windowSpacingSide"] + args["windowSize"][0])
        ):
            xPattern = 0
        for y in range(height):
            yPattern += 1
            if yPattern >= (
                2 * int(args["windowSpacingTopBot"] + args["windowSize"][1])
            ):
                yPattern = 0
            if (
                windowArea[0][0] <= xPattern < windowArea[1][0]
                and windowArea[0][1] <= yPattern < windowArea[1][1]
            ):
                main.setBlock(
                    "white_concrete",
                    (lines[x][0], lines[x][1] + y, lines[x][2]),
                )


def towerBalcony(XYZ, height, orientation=None, args=None, blocks=None):
    """
    [summary]

    Args:
        XYZ (List of lists): [description]
        height (int): [la hauteur ?]
        orientation ([type]): [north south east west]
        args ([type]): [to be defined]
        blocks ([type]): [description]
    """

    lines = []
    for i in range(len(XYZ) - 1):
        line = maths.line(XYZ[i], XYZ[i + 1], pixelPerfect=True)
        lines.extend(line)  # To be cleaned

    for x in range(len(lines)):
        if x % 2 == 0:
            main.setBlock("white_concrete", lines[x])
        else:
            main.setBlock("black_concrete", lines[x])


class Patterns:
    def __init__(self, patternData, XYZ):
        self.patternData = patternData
        self.XYZ = XYZ


if __name__ == "__main__":
    # simpleWindowPattern(
    #     [(-440, 64, 190), (-469, 69, 204), (-483, 71, 199)],
    #     4,
    #     simpleWindowPattern1,
    # )

    # towerBalcony(
    #     [(-422, 62 + 5, 158), (-455, 66 + 5, 141), (-485, 64 + 5, 164)], 5
    # )

    pillars = {
        "blackstone_wall": 1,
        "air": 5,
    }

    # randomPattern(
    #     [(-399, 66, 180), (-429, 72, 120), (-449, 69, 138)],
    #     4,
    #     5,
    #     "north",
    #     "horizontal",
    #     blocks,
    # )

    def balcony(XYZ, stages):

        for stage in range(stages):

            pillars = {
                "blackstone_wall": 1,
                "air": 5,
            }

            regularPattern(
                add_to_tuple(XYZ, 0, 6 * stage, 0),
                4,
                1,
                "west",
                "horizontal",
                pillars,
            )

            wall = {
                "red_concrete": 2,
                "red_terracotta": 1,
                "pink_terracotta": 1,
            }

            randomPattern(
                add_to_tuple(XYZ, 0, -2 + 6 * stage, -1),
                3,
                1,
                "north",
                "all",
                wall,
            )

            ground = {
                "andesite": 4,
                "stone": 2,
                "polished_andesite": 1,
            }

            randomPattern(
                add_to_tuple(XYZ, 0, -2 + 6 * stage, 0),
                2,
                4,
                "south",
                "all",
                ground,
            )

            glass = {
                "black_stained_glass": 2,
                "gray_stained_glass": 1,
            }

            randomPattern(
                add_to_tuple(XYZ, 0, 6 * stage, 3),
                4,
                1,
                "south",
                "horizontal",
                glass,
            )

    balcony([(-473, 63, 169), (-530, 63, 155)], 8)