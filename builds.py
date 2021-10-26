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
    "glass": {0: {"black_stained_glass_pane": 1}}, # Not correct structure, "0:" should be removed
    "vertical_lines": {0: {"black_stained_glass_pane": 1}},
    "stairs": {0: {"stone": 3, "andesite": 1}},
}


######################### Additional Functions #########################


def setPattern(pat, xyz):
    pass


examplePattern = {
    0:{0: {"block": "white_concrete", "args": {}}},
    1:{},
    2:{},
    3:{},
    4:{},
    5:{},
    6:{},
}


########################## Sections Functions ##########################
"""
connectedAreas defines the areas where the section is connected to
another, areas that should not be built. 2D, on the surface of the
corners area.
intersectionAreasExample = (((1, 2, 3), (4, 5, 6)), ((1, 2, 3), (4, 5, 6)))

Each functions here can be called independently. They must have all
the necessary arguments to be used by the user.

In the future, instead of having multiple functions for each different
patterns, we will have one that will generate different patterns.

Generate the façade. Should supports diagonals by knowing how to divide 
the patterns.
"""


def baseResidentialTower(
    corners, connectedAreas, height, blocks=residential_tower_materials
):
    # Generate the base here.
    pass


def middleResidentialTower(
    corners, connectedAreas, height, blocks=residential_tower_materials
):
    for facade in range(len(corners)):
        next = facade + 1
        if facade + 1 == len(corners):
            next = 0

        stage = 0
        for y in range(height[0], height[1]):
            stage += 1
            line = maths.line((corners[facade][0], y, corners[facade][1]), (corners[next][0], y, corners[next][1]))

            pat = 0
            n = 0
            for i in range(len(line)):
                if n >= 6:
                    n = 0
                    pat += 1
                n += 1

                if stage % 7 != 0:
                    main.setBlock("gray_stained_glass", line[i])

                if stage % 7 == 0 and n != 1:
                    main.setBlock("light_gray_concrete", line[i])
                    main.setBlock("light_gray_concrete", (line[i][0], int(line[i][1])-1, line[i][2]))

                if n == 1:
                    main.setBlock("white_concrete", line[i])
                    
                    if (line[i][0] != corners[facade][0] and line[i][2] != corners[facade][1]) and (line[i][0] != corners[next][0] and line[i][2] != corners[next][1]):
                        xz = maths.perpendicular(3, (line[i][0], line[i][2]), (corners[facade][0], corners[facade][1]))
                        print((xz[0][0], line[i][1], xz[0][1]))
                        main.setBlock("white_concrete", (xz[0][0], line[i][1], xz[0][1]))
                        main.setBlock("white_concrete", (xz[1][0], line[i][1], xz[1][1]))

                if n == 4:
                    xz = maths.perpendicular(3, (line[i][0], line[i][2]), (corners[facade][0], corners[facade][1]))
                    main.setBlock("black_stained_glass_pane", (xz[0][0], line[i][1], xz[0][1]))


def middleResidentialTower1(
    corners, connectedAreas, height, blocks=residential_tower_materials
):
    for facade in range(len(corners)):
        next = facade + 1
        if facade + 1 == len(corners):
            next = 0

        stage = 0
        for y in range(height[0], height[1]):
            stage += 1
            line = maths.line((corners[facade][0], y, corners[facade][1]), (corners[next][0], y, corners[next][1]))

            pat = 0
            n = 0
            for i in range(len(line)):
                if n >= 6:
                    n = 0
                    pat += 1
                n += 1

                if stage % 7 != 0:
                    main.setBlock("gray_stained_glass", line[i])

                if stage % 7 == 0 and n != 1:
                    main.setBlock("light_gray_concrete", line[i])
                    main.setBlock("light_gray_concrete", (line[i][0], int(line[i][1])-1, line[i][2]))

                if n == 1:
                    main.setBlock("white_concrete", line[i])
                    
                    if (line[i][0] != corners[facade][0] and line[i][2] != corners[facade][1]) and (line[i][0] != corners[next][0] and line[i][2] != corners[next][1]):
                        xz = maths.perpendicular(3, (line[i][0], line[i][2]), (corners[facade][0], corners[facade][1]))
                        print((xz[0][0], line[i][1], xz[0][1]))
                        main.setBlock("white_concrete", (xz[0][0], line[i][1], xz[0][1]))
                        main.setBlock("white_concrete", (xz[1][0], line[i][1], xz[1][1]))

                if n == 4:
                    xz = maths.perpendicular(3, (line[i][0], line[i][2]), (corners[facade][0], corners[facade][1]))
                    main.setBlock("black_stained_glass_pane", (xz[0][0], line[i][1], xz[0][1]))


def stairsResidentialTower(
    corners, connectedAreas, height, blocks=residential_tower_materials, exit="north"
):
    # Generate the stairs here.
    pass


def topResidentialTower(
    corners,
    connectedAreas,
    height,
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

        # TODO: Find each connected area between all the sections.
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

Define the global structure of the tower. A tower is divided into 
different sections. Each section is defined by points, that creates the 
shape viewed from above, and the start and end altitudes of this specific 
shape. A style (type) is also defined for this section. 
"""


towerData_example = {
    "base": {
        "type": baseResidentialTower,
        "corners": ((0, 0), (0, 30), (30, 30), (30, 0)),
        "height": (0, 10),
        "args": {"materials": residential_tower_materials},
    },
    "middle": {
        "type": middleResidentialTower,
        "corners": ((5, 5), (5, 25), (25, 25), (25, 5)),
        "height": (10, 50),
        "args": {"materials": residential_tower_materials},
    },
    "stairs": {
        "type": stairsResidentialTower,
        "corners": ((5, 5), (25, 5), (25, 0), (5, 0)),
        "height": (0, 17),
        "args": {
            "materials": residential_tower_materials,
        },
    },
    "top": {
        "type": topResidentialTower,
        "corners": ((5, 5), (5, 25), (25, 60, 25), (25, 5)),
        "height": (50, 60),
        "args": {
            "materials": residential_tower_materials,
            "greenFactor": 1,
            "modernFactor": 1,
        },
    },
}


if __name__ == "__main__":
    # tower = Tower(towerData_example)
    middleResidentialTower1(
    ((-703, -201), (-696, -181), (-716, -166), (-730, -174)), (), (71, 71+80), blocks=residential_tower_materials)

"""
Inputs simple building:
    n points (2d)                   set the global shape
    height min, max                 define the height
    type                            set the patterns that will be applied to the façade defined by the points above
    materials                       because a pattern can have different color palette
    args                            size of windows? green factor? ... relative to type
-> Create a decorated box.


Inputs complex buildings:
    n Inputs simple buildings       for each "section". TODO: Harmonize all the patterns to get continuity.
    type                            set the type of building. These will change the way it generates the interior structure and manage the accessibility.
    materials                       because each type uses some blocks palette to connect the areas.
    args                            number of stairs, elevators? ...
-> Take some decorated boxes, remove the intersections parts, fill the gaps differently depending of the type, manage the interior, create accessibility.

TODO: Find how to detect intersection between many polygons in 2d.
TODO: Divide spaces, create ways.

Procedural Gen:
    Create boxes and set it the best way possible. Use presets of type and matrials that go well together and that correspond to the city blocks. Sizes of boxes also depends of it.

TODO: "cleanLine" like for angles. Draw a line, count the number of blocks. For 1 block for example, draw a line from 0 to 1 meters, and only place the first block that is not on the origin. 
"""

"""
TODO List: (curve shape and/or polygon shape)

*Train Station
*Track
*Subway
*Tunnel

*Road
*Bridge
*Intersection
*Highway
*Highway Interchange
*Highway Exit
Bus Lane
Bicycle Path

Bus Stop
*Pedestrian Crossing
*Traffic Light
*Street Light
Bench
Park
Tree
Bin
*Electric cable

*Skyscraper
*Residential Tower
Apartment
Semi-detached House
*House
Villa
Hotels

Swimming Pool
School
*Hospital
Police Department
Fire Department
*Shopping Center
Prison
*Port
Airport
Marina
Farm
Military Base

Industrial District
Nuclear Power Station
Oil Platform
Wind Turbine
Solar Panel
Barrage
Field

Parking
Garage
Gas Station

Observatory
Antenna
"""

"""
TODO Buildings:

Info:                               style of the city district(richness, culture... -> != patterns, sizes of rooms, decorations...), materials preset.
Complex Patterns Manager            support diagonal ("cleanLine" for angles), adaptable/responsive, modifiable materials
# Façades Creator                     
Buildings Generator                 manage different boxes. Should understand where patterns stop to (divide them and to) generate them properly. ("polygon interconnected areas/intersections")
                                    ex: know if an angle is too small to put windows and in this case, cut the edge and replace the window pattern by a wall/bay window.
Structure Generator                 take data(coordinates of corners) from Building Generator and generate interior structure + foundations. Take care of balancing/wind?/accessibility. Generate stairs/corridors/elevators/rooms.
Decorator                           create the decoration for the rooms. Take data(coordinates of rooms) from Structure Generator. Large preset of decorations, categorized depending of the style/richness/room... A lot of condition for placing. TODO: A function to save MC Decoration as txt? file with tags...
"""

"""
TODO City Builder:

/setbuildarea                       defined the maximum range of the city.
run                                 generate an heightmap
edit                                paint with != color on the heightmap. Color and what they represent are in the legend. Can represent a district/park/main roads?/train line?
                                    ex: districts map, roads map, density map, subway map, temperature map? wind map? pollution map? weather map? richness map?
generate                            generate the buildings/interior structure/decoration/public development/street decoration/road quality depending of the maps. Place building between the predefined roads.
"""

"""
Names

Worlds Gen
Cities Gen
Minecraft Worlds Gen
Minecraft Worlds Generator
Minecraft Cities Gen
Minecraft Cities Generator

Monde Mod
Wind Mod
Weather Mod

Monde Mod: Weather
Monde Mod: Wind
Monde Gen: Cities
Monde Gen: Landscapes


Minecraft Monde Mod: Weather
Minecraft Monde Mod: Wind
Minecraft Monde Mod: Water/Waves/Wild
Minecraft Monde Gen: Cities
Minecraft Monde Gen: Landscapes

Project Horizon

MineMondeMod

HunterZ 2.0
"""

"""
Mods:

Waves                               Change dynamically the color of water to create waves / Create real waves.
Sands                               Add quicksand (snow power), water sand (different color and propriety depending of the water, compatible with Waves), smooth sand (sand carpet, that slows the player and that lets the player fall inside), particles (compatible with Wind), sandstorms (with Weather), moving dunes in the desert?
Winds                               Add wind particles, wind physics for entity, new weather (with Weather), wind simulation on the map
Weather                             Smooth the changes in the weather, add clouds, storm, snow storm, sandstorm (with Sand), != levels of rain...
Wild                                More flowers, grass... more animals, birds?
Pathogen                            Mushroom virus, blocks deterioration, virus propagation, vaccine, player contamination, spores, gas mask, new zombies, zombies based on players, better mob spawning
Winters                             New seasons, tree modification, mob spawn modification, modify(Temperature, Weather, Wind, Wild, Pathogen), real snow power (like smooth sand)
Dynamic World                       Change the world through seasons (Winter), change snow and ice on mountain, dune in the desert (Sands), regenerate forests, burn forests (Fires), destroy grief but don't repair buildings
Fire                                Better fire propagation, burnt blocks, smoke (Wind), extinguisher
Thirst                              Fresh water, filters, temperature, efforts
Weapon                              Craft, bullet time/drop, != damage depending on the hit point, torch light, modular guns, durability, ammunitions, bows, cuts
Blood                               Dynamic blood trace and projection after damage. Zombie attracted by blood?
Armed Concrete                      Possibility to lock zones/create safe zone. Block has multiple durability and need something to be break
Radio                               Add radiocommunication, vocal chat, radio, radioactivity...
Electricity                         Redstone need to be near a generator to be powered, the generator need to be powered by electricity, with cables...
Vehicles                            Cars, planes, train, subway, elevators?, boats, helicopters
Backpacks and Inventory             Add backpacks, with 3D models/blocks, with real interior for item storage, modify the inventory to be realistic, with item weight and size. Blocks are no longer transportable, or with a tools?
Trees                               Trees falls, grew up. Trunk of multiple blocks can be hold by multiple players?
Torch                               Torch turn off after a time (or in inventory), campfire too.
More Move                           Don't add double jump but more positions possible to the player and to zombies?
"""