import main
import maths
import interfaceUtils as minecraft

####################### Towers Materials Presets #######################
"""
0, 1... are for multiple materials, if there are. (like != type of
stairs)
"""


residential_tower_materials = {
    "structure": {
        0: {"stone": 3, "andesite": 1},
        1: {"white_concrete": 1},
        2: {"light_gray_concrete": 1},
    },
    "glass": {0: {"black_stained_glass_pane": 1}},
    "vertical_lines": {0: {"black_stained_glass_pane": 1}},
    "stairs": {0: {"stone": 3, "andesite": 1}},
}


######################### Additional Functions #########################


def findIntersectionAreas(box0, box1):
    minX, maxX = min(box1[0][0], box1[1][0]), max(box1[0][0], box1[1][0])
    minY, maxY = min(box1[0][1], box1[1][1]), max(box1[0][1], box1[1][1])
    minZ, maxZ = min(box1[0][2], box1[1][2]), max(box1[0][2], box1[1][2])

    points = [
        (minX, minY, minZ),
        (minX, minY, maxZ),
        (minX, maxY, maxZ),
        (minX, maxY, minZ),
        (maxX, maxY, maxZ),
        (maxX, maxY, minZ),
        (maxX, minY, minZ),
        (maxX, minY, maxZ),
    ]

    print("Points: ", points)
    for point in points:
        if (
            (
                min(box0[0][0], box0[1][0])
                <= point[0]
                <= max(box0[0][0], box0[1][0])
            )
            and (
                min(box0[0][1], box0[1][1])
                <= point[1]
                <= max(box0[0][1], box0[1][1])
            )
            and (
                min(box0[0][2], box0[1][2])
                <= point[2]
                <= max(box0[0][2], box0[1][2])
            )
        ):  # The point is inside the box.
            print("Intersection: ", point)
            main.setBlock("stone", point)


########################## Sections Functions ##########################
"""
intersectionAreas defines the areas where the section is connected to
another, areas that should not be built. 2D, on the surface of the
corners area.
intersectionAreasExample = (((1, 2, 3), (4, 5, 6)), ((1, 2, 3), (4, 5, 6)))

Each functions here can be called independently. They must have all
the necessary arguments to be used by the user.

In the future, instead of having multiple functions for each different
patterns, we will have one that will generate different patterns.
"""


def baseResidentialTower(
    corners, connectedAreas, blocks=residential_tower_materials
):
    # Generate the base here.
    pass


def middleResidentialTower(
    corners, connectedAreas, blocks=residential_tower_materials
):
    # Generate the middle here.
    pass


def stairsResidentialTower(
    corners, connectedAreas, blocks=residential_tower_materials, exit="north"
):
    # Generate the stairs here.
    pass


def topResidentialTower(
    corners,
    connectedAreas,
    blocks=residential_tower_materials,
    greenFactor=1,
    modernFactor=1,
):
    # Generate the top here.
    pass


########################### Towers Generator ###########################
"""
Call each function to generate the tower based on towerData. Do some
basic calculations to fill the missing arguments for the functions.
Generate the interior structure.
"""


class Tower:
    def __init__(self, towerData):
        self.towerData = towerData

        # Find each connected area between all the sections.
        # Top: Define exit.

        for __, section in enumerate(self.towerData):
            print(" ")
            for __, corners in enumerate(self.towerData):
                if corners != section:
                    findIntersectionAreas(
                        self.towerData[section]["corners"],
                        self.towerData[corners]["corners"],
                    )
                    print(self.towerData[section]["corners"], "---")
                    print(self.towerData[corners]["corners"])


############################ Towers Presets ############################
"""
towerData. Can be used by the user to generate a full tower. Later, an
other program should set all the values automatically.
"""


towerData_example = {
    "base": {
        "type": baseResidentialTower,
        "corners": ((0, 0, 0), (30, 10, 30)),
        "args": {"materials": residential_tower_materials},
    },
    "middle": {
        "type": middleResidentialTower,
        "corners": ((5, 10, 5), (25, 50, 25)),
        "args": {"materials": residential_tower_materials},
    },
    "stairs": {
        "type": stairsResidentialTower,
        "corners": ((5, 17, 5), (25, 0, 0)),
        "args": {
            "materials": residential_tower_materials,
        },
    },
    "top": {
        "type": topResidentialTower,
        "corners": ((5, 50, 5), (25, 60, 25)),
        "args": {
            "materials": residential_tower_materials,
            "greenFactor": 1,
            "modernFactor": 1,
        },
    },
}


if __name__ == "__main__":
    tower = Tower(towerData_example)
