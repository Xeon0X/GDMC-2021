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
    """
    A construction function that generates continuous lines of random
    blocks.

    Args:
        XYZ (list of tuples): List of coordinates in 3D. Must define
        a line that does not change direction and has a regular course.
        height (int): A positive integer representing the height, the y
        axis.
        width (int): A positive integer representing the width, the x or
        z direction depending on the orientation.
        orientation (str): "north", "south", "east", "west", where the
        side of the line is oriented.
        randomType (str): "all" for no pattern, "vertical" to have the
        same blocks on the same y coordinate, creating a vertical
        pattern. "horizontal instead.
        blocks (dict): A dictionary with blocks as keys and weight in
        random choices as values.
    """
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
    """
    A construction function that generates a pattern.

    Args:
        XYZ (list of tuples): List of coordinates in 3D. Must define
        a line that does not change direction and has a regular course.
        height (int): A positive integer representing the height, the y
        axis.
        width (int): A positive integer representing the width, the x or
        z direction depending on the orientation.
        orientation (str): "north", "south", "east", "west", where the
        side of the line is oriented.
        patternType (str): "vertical" to have the pattern applied on the
        same y coordinate, creating a vertical pattern. "horizontal
        instead.
        blocks (dict): A dictionary with blocks as keys and the number of
        times they appear as values.
    """
    line = combineLines(XYZ, pixelPerfect=True)
    pattern = dict_to_list(blocks)

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


if __name__ == "__main__":

    balcony([(-473, 63, 169), (-530, 63, 155)], 8)