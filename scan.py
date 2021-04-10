from worldLoader import WorldSlice
import numpy as np
import requests
import cv2
import maths
import random
import map
from PIL import Image
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.morphology import skeletonize


def heightmap(xzStart, xzDistance):  # TODO: Can be better and clear.
    """
    Generate a heightmap using nbt data.

    Args:
        xzStart (tuple): xz coordinates of the northwest corner of the
        area to scan.
        xzDistance (tuple): xz distance of the southwest corner from the
        northwest corner.

    Returns:
        heightmap.png

    >>> heightmap((-256, -256), (512, 512))
    """

    heightmap = Image.new(
        "RGBA",
        (xzDistance[0], xzDistance[1]),
        "red",
    )

    heightmapBiome = Image.new(
        "RGBA",
        (xzDistance[0], xzDistance[1]),
        "red",
    )

    slice = WorldSlice((xzStart[0], xzStart[1], xzDistance[0], xzDistance[1]))
    heightmapData = list(
        np.array(slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"], dtype=np.uint8)
    )

    for x in range(0, xzDistance[0]):
        for z in range(0, xzDistance[1]):
            y = heightmapData[x][z]
            biomeId = slice.getBiomeAt((xzStart[0] + x, 0, xzStart[1] + z))
            block = slice.getBlockAt((xzStart[0] + x, y, xzStart[1] + z))
            heightmapBiome.putpixel((x, z), heightmapColor(y, biomeId, block))
            heightmap.putpixel((x, z), (y, y, y))

    heightmap.save("heightmap.png")
    heightmapBiome.save("heightmap_biome.png")


def voronoiCoordinates(
    blocks, area, distanceMin1, distanceMin2
):  # TODO:Better
    xyz1, xyz2 = area
    xzStart, xzDistance = areaCoordinates(xyz1, xyz2)
    heightmap(xzStart, xzDistance)
    im = Image.open("heightmap.png")

    # Creating points depending of  the heightmap.
    buildable = []
    notBuildable = []
    notBuildable2 = []

    for x in range(0, xzDistance[0]):
        for z in range(0, xzDistance[1]):
            __, g, b = im.getpixel((x, z))
            if b >= 80:
                notBuildable2.append((xzStart[0] + x, xzStart[1] + z))
            elif g == 50:
                buildable.append((xzStart[0] + x, xzStart[1] + z))
            else:
                notBuildable.append((xzStart[0] + x, xzStart[1] + z))

    # Sorting points depending of the distance.
    coordsBuildable = []
    coordsNotBuildable = []
    coordsNotBuildable2 = []

    for build in buildable:
        if all(
            maths.distance2D(build, coord) > distanceMin1
            for coord in coordsBuildable
        ):
            coordsBuildable.append(build)

    for notBuild in notBuildable:
        if all(
            maths.distance2D(notBuild, coord) > distanceMin2
            for coord in coordsNotBuildable
        ):
            coordsNotBuildable.append(notBuild)

    for notBuild2 in notBuildable2:
        if all(
            maths.distance2D(notBuild2, coord) > distanceMin2
            for coord in coordsNotBuildable2
        ):
            coordsNotBuildable2.append(notBuild2)

    # Generating voronoi.
    zonesDistrictsPos = (
        [coordsBuildable] + [coordsNotBuildable] + [coordsNotBuildable2]
    )
    areaMinMax = (
        (min(area[0][0], area[1][0]), min(area[0][-1], area[1][-1])),
        (max(area[0][0], area[1][0]), max(area[0][-1], area[1][-1])),
    )
    print(areaMinMax)
    map.voronoi(blocks, areaMinMax, zonesDistrictsPos, xzStart)


def areaCoordinates(xyz1, xyz2):
    """
    Transform an area into a start point and a distance. Work with xyz
    coordinates and xz coordinates.

    Args:
        xyz1 (tuple): Coordinates, whatever the direction.
        xyz2 (tuple): Coordinates, whatever the direction.

    Returns:
        tuple: xzStart, xzDistance
    """
    xzStart = (min(xyz1[0], xyz2[0]), min(xyz1[-1], xyz2[-1]))
    xzDistance = (
        (abs(xyz1[0] - xyz2[0])),
        (abs(xyz1[-1] - xyz2[-1])),
    )
    return xzStart, xzDistance


def heightmapColor(y, biomeId, block):
    neutral = [
        16,
        26,
        13,
        12,
        129,
        1,
        3,
        131,
        162,
        2,
        17,
        37,
        39,
        35,
        36,
        163,
        164,
    ]
    water = [
        0,
        7,
        10,
        11,
        24,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
    ]

    waterBlocks = [
        "minecraft:water",
        "minecraft:seagrass",
        "minecraft:tall_seagrass",
        "minecraft:kelp_plant",
    ]

    if (biomeId in water) or (block in waterBlocks):
        return y, y, 255, y
    if biomeId in neutral:
        return y, 255, y, y
    else:
        return 255, y, y, y


def canny(image):
    # Open the image
    img = cv2.imread(image)

    # Apply Canny
    edges = cv2.Canny(img, 100, 200, 3, L2gradient=True)

    plt.figure()
    plt.title("Heightmap Test")
    plt.imsave("heightmap_canny.png", edges, cmap="gray", format="png")
    plt.imshow(edges, cmap="gray")
    plt.show()


# blocks = [
#     "minecraft:white_concrete",
#     "minecraft:red_concrete",
#     "minecraft:blue_concrete",
# ]
# voronoiCoordinates(blocks, ((15, 294), (-339, -39)), 70, 40)


def sobel(image):
    # Open the image
    img = np.array(Image.open(image)).astype(np.uint8)

    # Apply gray scale
    gray_img = np.round(
        0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    ).astype(np.uint8)

    # Sobel Operator
    h, w = gray_img.shape
    # define filters
    horizontal = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # s2
    vertical = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # s1

    # define images with 0s
    newhorizontalImage = np.zeros((h, w))
    newverticalImage = np.zeros((h, w))
    newgradientImage = np.zeros((h, w))

    # offset by 1
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            horizontalGrad = (
                (horizontal[0, 0] * gray_img[i - 1, j - 1])
                + (horizontal[0, 1] * gray_img[i - 1, j])
                + (horizontal[0, 2] * gray_img[i - 1, j + 1])
                + (horizontal[1, 0] * gray_img[i, j - 1])
                + (horizontal[1, 1] * gray_img[i, j])
                + (horizontal[1, 2] * gray_img[i, j + 1])
                + (horizontal[2, 0] * gray_img[i + 1, j - 1])
                + (horizontal[2, 1] * gray_img[i + 1, j])
                + (horizontal[2, 2] * gray_img[i + 1, j + 1])
            )

            newhorizontalImage[i - 1, j - 1] = abs(horizontalGrad)

            verticalGrad = (
                (vertical[0, 0] * gray_img[i - 1, j - 1])
                + (vertical[0, 1] * gray_img[i - 1, j])
                + (vertical[0, 2] * gray_img[i - 1, j + 1])
                + (vertical[1, 0] * gray_img[i, j - 1])
                + (vertical[1, 1] * gray_img[i, j])
                + (vertical[1, 2] * gray_img[i, j + 1])
                + (vertical[2, 0] * gray_img[i + 1, j - 1])
                + (vertical[2, 1] * gray_img[i + 1, j])
                + (vertical[2, 2] * gray_img[i + 1, j + 1])
            )

            newverticalImage[i - 1, j - 1] = abs(verticalGrad)

            # Edge Magnitude
            mag = np.sqrt(pow(horizontalGrad, 2.0) + pow(verticalGrad, 2.0))
            newgradientImage[i - 1, j - 1] = mag

    plt.figure()
    plt.title("heightmap.png")
    plt.imsave(
        "heightmap_sobel.png", newgradientImage, cmap="gray", format="png"
    )
    plt.imshow(newgradientImage, cmap="gray")


def edge(image):
    im = Image.open(image)
    width, height = im.size
    for x in range(width):
        for y in range(height):
            if im.getpixel((x, y))[0] >= 25:
                im.putpixel((x, y), (255, 255, 255))
    im.save("heightmap_edge.png")
    print("done")


def blur(image):
    # Blur
    img = cv2.imread(image)
    img = cv2.medianBlur(img, 5)
    plt.imsave("heightmap_medianBlur.png", img, cmap="gray", format="png")


def skeletonize(image):
    # Read the image as a grayscale image
    img = cv2.imread(image, 0)

    # Threshold the image
    ret, img = cv2.threshold(img, 127, 255, 0)

    # Step 1: Create an empty skeleton
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    # Get a Cross Shaped Kernel
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    # Repeat steps 2-4
    while True:
        # Step 2: Open the image
        open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
        # Step 3: Substract open from the original image
        temp = cv2.subtract(img, open)
        # Step 4: Erode the original image and refine the skeleton
        eroded = cv2.erode(img, element)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
        if cv2.countNonZero(img) == 0:
            break

    # Displaying the final skeleton
    cv2.imshow("Skeleton", skel)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


heightmap((-256, -256), (512, 512))
# sobel("heightmap.png")
# edge("heightmap_sobel.png")
# sobel("heightmap_edge.png")
# canny("heightmap_sobel.png")
blur("heightmap_biome.png")
skeletonize("heightmap_medianBlur.png")

print("DONE")