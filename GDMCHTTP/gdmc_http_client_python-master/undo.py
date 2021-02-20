import requests
from math import *
import numpy as np
import matplotlib.pyplot as plt

# Init
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
    x1,y1,z1,x2,y2,z2 = round(x1),round(y1),round(z1),round(x2),round(y2),round(z2)

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

    if (dx >= dy and dx >= dz): # Driving axis is X-axis
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

    elif (dy >= dx and dy >= dz): # Driving axis is Y-axis
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

    else: # Driving axis is Z-axis
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

# For 
# Smooth Curve
# https://towardsdatascience.com/b%C3%A9zier-interpolation-8033e9a262c2
def get_bezier_coef(points): # find the a & b points
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

def get_cubic(a, b, c, d): # returns the general Bezier cubic formula given 4 control points
    return lambda t: np.power(1 - t, 3) * a + 3 * np.power(1 - t, 2) * t * b + 3 * (1 - t) * np.power(t, 2) * c + np.power(t, 3) * d

def get_bezier_cubic(points): # return one cubic curve for each consecutive points
    A, B = get_bezier_coef(points)
    return [
        get_cubic(points[i], A[i], B[i], points[i + 1])
        for i in range(len(points) - 1)
    ]

def evaluate_bezier(points, n): # evalute each cubic curve on the range [0, 1] sliced in n points
    curves = get_bezier_cubic(points)
    return np.array([fun(t) for fun in curves for t in np.linspace(0, 1, n)])


points = np.array([[3423,-1690],[3402,-1652],[3500,-1654],[3457,-1703]])
path = evaluate_bezier(points, 50)
x, y = points[:,0], points[:,1]
px, py = path[:,0], path[:,1]

def test():
    # creation of lines-------------------------------------------
    y = 160
    line = []
    for i in range(0,len(px)-1):
        setBlock("air", (px[i], y+1, py[i]))
        setBlock("air", (px[i+1], y+2, py[i+1]))
        liste = []
        liste = mathLine((px[i], y, py[i]), (px[i+1], y, py[i+1]), 0)
        for i in liste:
            line.append(i)

    # creation of line2 without duplicates
    line2 = []
    for i in line:
        if i not in line2:
            line2.append(i)
    # print(len(line), len(line2))

    # detection of blocks near others on two sides
    line3 = []
    for i in range(1,len(line2)-1):
        if ((line2[i][0] == line2[i-1][0]) & (line2[i][2] == line2[i+1][2])) or ((line2[i][2] == line2[i-1][2]) & (line2[i][0] == line2[i+1][0])):
            # print(line2[i-1],line2[i],line2[i+1])
            line3.append(line2[i])
    # print(len(line3), line3)

    # removal of blocks near others on two sides
    print(line3)
    #for i in range(0,len(line3)):
        #setBlock('black_concrete', (line3[i][0],line3[i][1]-1,line3[i][2]))
    near = 0
    for i in range(1,len(line3)-1):
        print("//////////////////",line3[i])
        # Not side by side with an other : delete OK
        if (((line3[i][0] != line3[i-1][0]) & (line3[i][2] != line3[i-1][2])) or ((line3[i][2] != line3[i-1][2]) & (line3[i][0] != line3[i-1][0]))) & (((line3[i][0] != line3[i+1][0]) & (line3[i][2] != line3[i+1][2])) or ((line3[i][2] != line3[i+1][2]) & (line3[i][0] != line3[i+1][0]))):
            # print(line3[i],line3[i+1])
            #setBlock('black_concrete', (line3[i][0],line3[i][1]+1,line3[i][2]))
            line2.remove((line3[i]))
            print("1", line3[i-1],line3[i],line3[i+1])
        # Side by side with 2 other
        elif ( (line3[i][0] == line3[i-1][0]) & (sqrt(line3[i][2]**2 + line3[i-1][2]**2) == 1) & (line3[i][2] == line3[i+1][2]) & (sqrt(line3[i][0]**2 + line3[i+1][0]**2) == 1) )or( (line3[i][0] == line3[i+1][0]) & (sqrt(line3[i][2]**2 + line3[i+1][2]**2) == 1) & (line3[i][2] == line3[i-1][2]) & (sqrt(line3[i][0]**2 + line3[i-1][0]**2) == 1) )  :
            # print(line3[i],line3[i+1])
            #setBlock('black_concrete', (line3[i][0],line3[i][1]+1,line3[i][2]))
            line2.remove((line3[i]))
            print("2", line3[i-1],line3[i],line3[i+1])
        # Side by side with only 1 block
        elif ( (line3[i][0] == line3[i-1][0]) & ((line3[i][2] - line3[i-1][2]) in {1,-1}) )or( (line3[i][0] == line3[i+1][0]) & ((line3[i][2] - line3[i+1][2]) in {1,-1}) ):
            if near == 0:
                near += 1
                #setBlock('black_concrete', (line3[i][0],line3[i][1]+1,line3[i][2]))
                line2.remove((line3[i]))
                print("3", line3[i-1],line3[i],line3[i+1])
            else:
                near = 0
                print("***************************")

    line2.remove((line3[0]))
    line2.remove((line3[-1]))

    # Block cote a cote
    # ( ((line3[i][0] == line3[i-1][0]) & (sqrt(line3[i][2]**2 + line3[i-1][2]**2) == 1)) & ((line3[i][2] == line3[i+1][2]) & (sqrt(line3[i][0]**2 + line3[i+1][0]**2) == 1)) or ((line3[i][0] == line3[i+1][0]) & (sqrt(line3[i][2]**2 + line3[i+1][2]**2) == 1)) & ((line3[i][2] == line3[i-1][2]) & (sqrt(line3[i][0]**2 + line3[i-1][0]**2) == 1))  )

    # setBlock
    for i in range(0, len(line2)):
        setBlock('gold_block', (line2[i]))

    #setBlock("dirt", (188,63,127))
    #setLine("diamond_block", (188,63,127), (209,75,167), 1)-------------------------------------------

def pixelPerfect(path):
    print("a")
    if len(path) == 1 | len(path) == 0:
        return(path)
        print("b")
    pixelPerfect = []
    c = 0
    while c < len(path):
        print(c)
        if c > 0 & c+1 < len(path):
            print("d")
            if (path[c-1][0] == path[c][0] or path[c-1][2] == path[c][2]
            and path[c+1][0] == path[c][0] or path[c+1][2] == path[c][2]
            and path[c-1][2] != path[c+1][2]
            and path[c-1][2] != path[c+1][2]):
                print("------------")
                c += 1
                pixelPerfect.append(path[c])

def undo():
    with open(undoFile, 'r') as file:
        undoData = file.read()
        print(undoData)

path = mathLine((3446, 80, -1596),(3395, 80, -1667), 1)
for i in range(0, len(path)):
    setBlock('gold_block', (path[i]))

'''
perfect = pixelPerfect(path)
for i in range(0, len(perfect)):
    setBlock('diamond_block', (perfect[i]))
'''
undo()
# On prend le nombre de block entre tous les points et on les allignes. On leur hauteur pour les placer sur l autre axe. On calcule la courbe passant par ses points qui définissent l axe y.
#Appliquer un correction post gen est possible est assez simple : regle des 1-3-1 = 2-2-1, 2-2 = 1-1-1...