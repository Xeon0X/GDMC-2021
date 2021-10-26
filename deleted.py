# def maxXYZ(XYZ):
#     X, Y, Z = [], [], []
#     for xyz in XYZ:
#         X.append(xyz[0])
#         Y.append(xyz[1])
#         Z.append(xyz[2])

#     if (max(X), max(Y), max(Z)) in XYZ:
#         return (max(X), max(Y), max(Z))


# def minXYZ(XYZ):
#     X, Y, Z = [], [], []
#     for xyz in XYZ:
#         X.append(xyz[0])
#         Y.append(xyz[1])
#         Z.append(xyz[2])

#     if (min(X), min(Y), min(Z)) in XYZ:
#         return (min(X), min(Y), min(Z))


# def findIntersectionAreas(box0, box1):
#     minX, maxX = min(box1[0][0], box1[1][0]), max(box1[0][0], box1[1][0])
#     minY, maxY = min(box1[0][1], box1[1][1]), max(box1[0][1], box1[1][1])
#     minZ, maxZ = min(box1[0][2], box1[1][2]), max(box1[0][2], box1[1][2])

#     points = [
#         (minX, minY, minZ),
#         (minX, minY, maxZ),
#         (minX, maxY, maxZ),
#         (minX, maxY, minZ),
#         (maxX, maxY, maxZ),
#         (maxX, maxY, minZ),
#         (maxX, minY, minZ),
#         (maxX, minY, maxZ),
#     ]

#     connectedAreas = []
#     for point in points:
#         if (
#             (
#                 min(box0[0][0], box0[1][0])
#                 <= point[0]
#                 <= max(box0[0][0], box0[1][0])
#             )
#             and (
#                 min(box0[0][1], box0[1][1])
#                 <= point[1]
#                 <= max(box0[0][1], box0[1][1])
#             )
#             and (
#                 min(box0[0][2], box0[1][2])
#                 <= point[2]
#                 <= max(box0[0][2], box0[1][2])
#             )
#         ):  # The point is inside the box.
#             print("Intersection: ", point)
#             main.setBlock("stone", point)
#             connectedAreas.append(point)

#     maxCorner = maxXYZ(connectedAreas)
#     minCorner = minXYZ(connectedAreas)

#     # HERE

