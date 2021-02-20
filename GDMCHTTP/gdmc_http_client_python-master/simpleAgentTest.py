import requests
from math import *
import numpy as np
url = 'http://localhost:9000/command'

def runCommand(command):
    print("running cmd %s" % command)
    response = requests.post(url, bytes(command, "utf-8"))
    return response.text

# With runCommand
def setBlock(block, pos):
    print(runCommand(f"setblock %i %i %i {block}" % tuple(pos)))

# With runCommand, setBlock, mathLine
def setLine(block, pos1, pos2, parameter):
    points = mathLine(pos1, pos2, parameter)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))

# For setLine
# Code for generating points on a 3-D line using Bresenham's Algorithm
# https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/
def mathLine(pos1, pos2, parameter):

    (x1,y1,z1) = pos1
    (x2,y2,z2) = pos2

    ListOfPoints = [] 
    ListOfPoints.append((x1, y1, z1)) 
    dx = abs(x2 - x1) 
    dy = abs(y2 - y1) 
    dz = abs(z2 - z1) 
    if (x2 > x1): 
        xs = 1
    else: 
        xs = -1
    if (y2 > y1): 
        ys = 1
    else: 
        ys = -1
    if (z2 > z1): 
        zs = 1
    else: 
        zs = -1

    # Driving axis is X-axis" 
    if (dx >= dy and dx >= dz):         
        p1 = 2 * dy - dx 
        p2 = 2 * dz - dx 
        while (x1 != x2): 
            x1 += xs
            ListOfPoints.append((x1, y1, z1))
            if (p1 >= 0): 
                y1 += ys
                if parameter == 1:
                    if ListOfPoints[-1][1] != y1: 
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dx 
            if (p2 >= 0): 
                z1 += zs
                if parameter == 1:
                    if ListOfPoints[-1][2] != z1:
                        ListOfPoints.append((x1, y1, z1)) 
                p2 -= 2 * dx 
            p1 += 2 * dy 
            p2 += 2 * dz 

    # Driving axis is Y-axis" 
    elif (dy >= dx and dy >= dz):        
        p1 = 2 * dx - dy 
        p2 = 2 * dz - dy 
        while (y1 != y2): 
            y1 += ys
            ListOfPoints.append((x1, y1, z1))
            if (p1 >= 0): 
                x1 += xs
                if parameter == 1:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dy 
            if (p2 >= 0):
                z1 += zs
                if parameter == 1:
                    if ListOfPoints[-1][2] != z1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dy 
            p1 += 2 * dx 
            p2 += 2 * dz  

    # Driving axis is Z-axis" 
    else:         
        p1 = 2 * dy - dz 
        p2 = 2 * dx - dz 
        while (z1 != z2): 
            z1 += zs
            ListOfPoints.append((x1, y1, z1))
            if (p1 >= 0): 
                y1 += ys
                if parameter == 1:
                    if ListOfPoints[-1][1] != y1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dz 
            if (p2 >= 0): 
                x1 += xs 
                if parameter == 1:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dz 
            p1 += 2 * dy 
            p2 += 2 * dx
    return ListOfPoints

import numpy as np
import matplotlib.pyplot as plt

# find the a & b points
def get_bezier_coef(points):
    # since the formulas work given that we have n+1 points
    # then n must be this:
    n = len(points) - 1

    # build coefficents matrix
    C = 4 * np.identity(n)
    np.fill_diagonal(C[1:], 1)
    np.fill_diagonal(C[:, 1:], 1)
    C[0, 0] = 2
    C[n - 1, n - 1] = 7
    C[n - 1, n - 2] = 2

    # build points vector
    P = [2 * (2 * points[i] + points[i + 1]) for i in range(n)]
    P[0] = points[0] + 2 * points[1]
    P[n - 1] = 8 * points[n - 1] + points[n]

    # solve system, find a & b
    A = np.linalg.solve(C, P)
    B = [0] * n
    for i in range(n - 1):
        B[i] = 2 * points[i + 1] - A[i + 1]
    B[n - 1] = (A[n - 1] + points[n]) / 2

    return A, B

# returns the general Bezier cubic formula given 4 control points
def get_cubic(a, b, c, d):
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

# return one cubic curve for each consecutive points
def get_bezier_cubic(points):
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

# evalute each cubic curve on the range [0, 1] sliced in n points
def evaluate_bezier(points, n):
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])


points = np.array([[209,167],[213,128],[245,126]])
path = evaluate_bezier(points, 10)
x, y = points[:,0], points[:,1]
px, py = round(path[:,0]), round(path[:,1])
print(px, py, x, y)

y= 80
for i in range(0,len(px)-1):
    setLine("concrete", (px[i], y, py[i]), (px[i+1], y, py[i+1]), 0)
setLine("concrete", (px[-1], y, py[-1]), (px[1], y, py[1]), 0)

setBlock("dirt", (188,63,127))
#setLine("diamond_block", (188,63,127), (209,75,167), 1)