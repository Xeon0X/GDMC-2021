'''SETUP'''

import requests
from math import *
import numpy as np
import matplotlib.pyplot as plt

url = 'http://localhost:9000/command'

'''BASE COMMANDS'''

def runCommand(command):
    print("running cmd %s" % command)
    response = requests.post(url, bytes(command, "utf-8"))
    return response.text

# With runCommand
def setBlock(block, pos):
    print(runCommand(f"setblock %i %i %i {block}" % tuple(pos)))

# With runCommand, setBlock, mathLine
def setLine(block, pos1, pos2, pixelPerfect=True):
    points = mathLine(pos1, pos2, pixelPerfect)

    for i in points:
        setBlock(block, (i[0], i[1], i[2]))

# For setLine
# Code for generating points on a 3-D line using Bresenham's Algorithm
# https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/
def mathLine(pos1, pos2, pixelPerfect=1):

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
                if pixelPerfect == 1:
                    if ListOfPoints[-1][1] != y1: 
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dx 
            if (p2 >= 0): 
                z1 += zs
                if pixelPerfect == 1:
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
                if pixelPerfect == 1:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dy 
            if (p2 >= 0):
                z1 += zs
                if pixelPerfect == 1:
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
                if pixelPerfect == 1:
                    if ListOfPoints[-1][1] != y1:
                        ListOfPoints.append((x1, y1, z1))
                p1 -= 2 * dz 
            if (p2 >= 0): 
                x1 += xs 
                if pixelPerfect == 1:
                    if ListOfPoints[-1][0] != x1:
                        ListOfPoints.append((x1, y1, z1))
                p2 -= 2 * dz 
            p1 += 2 * dy 
            p2 += 2 * dx
    return ListOfPoints

'''ROADS'''

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



def pixelPerfect(path):
    ''' pixelPerfect
    '''

    # notPixelPerfect detection
    if len(path) == 1 or len(path) == 0:
        return(path)
    else:
        notPixelPerfect = []
        c = 0
        while c < len(path):
            if c > 0 and c+1 < len(path):
                if ((path[c-1][0] == path[c][0] or path[c-1][1] == path[c][1]) and \
                    (path[c+1][0] == path[c][0] or path[c+1][1] == path[c][1]) and \
                    path[c-1][1] != path[c+1][1] and \
                    path[c-1][0] != path[c+1][0]):
                    notPixelPerfect.append(path[c])
            c += 1
    
    # double notPixelPerfect detection
    if len(notPixelPerfect) == 1 or len(notPixelPerfect) == 0:
        return(notPixelPerfect)
    else:
        d = 0
        while d < len(notPixelPerfect):
            if d+1 < len(notPixelPerfect):
                if ((notPixelPerfect[d][0] == notPixelPerfect[d+1][0] and \
                    (notPixelPerfect[d][1] - notPixelPerfect[d+1][1]) in {1, -1}) or \
                    (notPixelPerfect[d][1] == notPixelPerfect[d+1][1] and \
                    (notPixelPerfect[d][0] - notPixelPerfect[d+1][0]) in {1, -1})):
                    notPixelPerfect.remove(notPixelPerfect[d+1])
            d += 1
    
    # remove notPixelPerfect from path
    for i in range(len(notPixelPerfect)):
        path.remove(notPixelPerfect[i])
    
    return(path)

def OLDcleanLine(path):
    removeLine = []
    addLine = []
    modif = 0
    # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block
    for i in range(0,len(path)-3):
        if (path[i][0] == path[i+1][0] and path[i+2][1] == path[i+3][1]):
            removeLine.append(path[i+1])
            removeLine.append(path[i+2])
            addLine.append((path[i+2][0],path[i+1][1]))
            modif += 1
        if (path[i][1] == path[i+1][1] and path[i+2][0] == path[i+3][0]):
            removeLine.append(path[i+1])
            removeLine.append(path[i+2])
            addLine.append((path[i+1][0],path[i+2][1]))
            modif += 1
    
    for i in range(1, len(path)-5):
        # 1 block, 3 blocks, 1 block = 1 block, 2 blocks, 2 blocks
        if (path[i+1][1] == path[i+2][1] and path[i+2][1] == path[i+3][1]) and \
            (path[i+1][1] != path[i][1] and path[i+3][1] != path[i+4][1]) and \
            (path[i-1][0] != path[i][0] and path[i+4][0] != path[i+5][0]):
            removeLine.append(path[i+1])
            modif += 1
            addLine.append((path[i+1][0],path[i][1]))
        if (path[i+1][0] == path[i+2][0] and path[i+2][0] == path[i+3][0]) and \
            (path[i+1][0] != path[i][0] and path[i+3][0] != path[i+4][0]) and \
            (path[i-1][1] != path[i][1] and path[i+4][1] != path[i+5][1]):
            removeLine.append(path[i+1])
            addLine.append((path[i][0],path[i+1][1]))
            modif += 1
    # for i in range(4, len(path)-1):
    #     # 4 blocks, 1 block = 3 blocks, 2 blocks STOP HERE ---------------- revoir pour éviter les cas particulier avec des blocks pas cote a cote # A revoir
    #     if (path[i-1][1] != path[i][1]) and \
    #         ((path[i-1][1] == path[i-2][1]) and (path[i-2][1] == path[i-3][1]) and (path[i-3][1] == path[i-4][1])) and \
    #         (path[i+2][1] != path[i][1]) and (path[i-][1] != path[i-1][1])
    #         removeLine.append(path[i-1])
    #         addLine.append((path[i-1][0],path[i][1]))

    return(removeLine, addLine, modif)

def cleanLine(path): # WORK BUT NOT ENDS
    ''' clean and smooth a list of blocks coordinates:
    '''

    i = 0
    while i < len(path):
        # for j in range(i-10,i):
        #     if i % 2 == 0:
        #         setBlock('green_stained_glass', (path[j][0], 112, path[j][1]))
        #     else:
        #         setBlock('blue_stained_glass', (path[j][0], 112, path[j][1]))
        # print("C")
        # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block
        if i+3 < len(path):
            if (path[i][0] == path[i+1][0] and path[i+2][1] == path[i+3][1]):
                path.insert((i+1), (path[i+2][0],path[i+1][1]))
                del path[i+2] # 2nd block
                del path[i+2] # 3rd block
                i -= 10
                print("A")
                continue
            elif (path[i][1] == path[i+1][1] and path[i+2][0] == path[i+3][0]):
                path.insert((i+1), (path[i+1][0],path[i+2][1]))
                del path[i+2] # 2nd block
                del path[i+2] # 3rd block
                i -= 10
                print("B")
                continue
        
        # 1 block, 3 blocks, 1 block = 1 block, 2 blocks, 2 blocks
        if i-1 >= 0 and i+5 <= len(path):
            print("1")
            if (path[i+1][1] == path[i+2][1] and path[i+2][1] == path[i+3][1]) and \
            (path[i+1][1] != path[i][1] and path[i+3][1] != path[i+4][1]) and \
            (path[i-1][1] != path[i][1] and path[i+4][1] != path[i+5][1]):
                path.insert((i+1), (path[i+1][0],path[i][1]))
                del path[i+2] # 2nd block
                i -= 10
                print("2")
                continue
            elif (path[i+1][0] == path[i+2][0] and path[i+2][0] == path[i+3][0]) and \
            (path[i+1][0] != path[i][0] and path[i+3][0] != path[i+4][0]) and \
            (path[i-1][0] != path[i][0] and path[i+4][0] != path[i+5][0]):
                path.insert((i+1), (path[i][0],path[i+1][1]))
                del path[i+2] # 2nd block
                i -= 10
                print("3")
                continue

        i += 1
    return(path)


#With pixelPerfect, mathLine
def smoothCurve(points, res=7):
    path = evaluate_bezier(points, res)
    x, z = points[:,0], points[:,2]
    px, pz = path[:,0], path[:,2]

    # creation of line in XZ with a random Y
    y = 205
    line = []
    for i in range(0,len(px)-1):
        setBlock('red_concrete', (px[i], 105, pz[i]))                                   # debug
        lineTemp = []
        lineTemp = mathLine((px[i], y, pz[i]), (px[i+1], y, pz[i+1]), 0)
        for i in lineTemp:
            line.append((i[0],i[2]))

    # creation of line2 without duplicates
    line2 = []
    for i in line:
        if i not in line2:
            line2.append(i)

    # pixel perfect
    line3 = []
    line3 = pixelPerfect(line2)
    for i in range(0,len(line3)):
        setBlock('red_stained_glass', (line3[i][0], 110, line3[i][1]))                     # debug
    
    line4 = cleanLine(line3)
    for i in range(0, len(line4)):
        setBlock('white_concrete', (line4[i][0], 195, line4[i][1]))

def newSmoothCurve(points, type, res=7):



    # First line (X, Z)
    # Initialization of points X,Z
    px, pz = initPoints(points,type,res)

    # LineCreationXZ
    line = lineCreationXZ(px, pz, y=0)

    # line2 = noDuplicates
    line2 = []
    for i in line:
        if i not in line2:
            line2.append(i)
    
    # pixelPerfect
    line3 = pixelPerfect(line2)

    # cleanLine
    line4 = cleanLine(line3)

    targets = []
    pointsList = points.tolist()
    for i in range(len(line4)):
        for j in range(len(pointsList)):
            if (line4[i][0] == pointsList[j][0]) and (line4[i][1] == pointsList[j][2]):
                targets.append([points[j][1], i])


    # Second line (len, Y)
    # Initialization of points len,Y
    targetsPoints = np.array(targets)
    px, py = initPoints(targetsPoints, type, res, 1)

    # LineCreationY
    lineY = lineCreationY(px, py, z=0)

    # lineY2 = noDuplicates
    lineY2 = []
    for i in lineY:
        if i not in lineY2:
            lineY2.append(i)
    
    # pixelPerfect
    lineY3 = lineY2

    # cleanLine
    lineY4 = cleanLine(lineY3)
    print(lineY4)
    print(len(lineY4))
    print(line4)
    print(len(line4))



    # Third Line : X,Y,Z
    curve = []
    if len(lineY4) <= len(line4):
        for i in range(len(lineY4)):
            curve.append([line4[i][0],lineY4[i][0], line4[i][1]])
    else:
        for i in range(len(line4)):
            curve.append([line4[i][0],lineY4[i][0], line4[i][1]])

    for i in range(len(curve)):
        setBlock('white_concrete', (curve[i][0], curve[i][1], curve[i][2]))

    curveY = []
    for i in range(len(targets)):
        curveY.append(targets[i][1])
        del targets[i][1]

    coorPerpendicularMid0, coorPerpendicularMid1 = offset(20, targets)
    for i in range(len(coorPerpendicularMid0)-1):
        setLine("cobweb", (coorPerpendicularMid0[i][0], curveY[i], coorPerpendicularMid0[i][1]), (coorPerpendicularMid0[i+1][0], curveY[i], coorPerpendicularMid0[i+1][1]))
        setLine("dirt", (coorPerpendicularMid1[i][0], curveY[i], coorPerpendicularMid1[i][1]), (coorPerpendicularMid1[i+1][0], curveY[i], coorPerpendicularMid1[i+1][1]))

    print(curve)



def lineCreationY(px, py, z=0):
    line = []
    for i in range(0,len(px)-1):
        lineTemp = mathLine((px[i], py[i], z), (px[i+1], py[i+1], z), 0)
        for i in lineTemp:
            line.append((i[0],i[1]))
    return(line)

def lineCreationXZ(px, pz, y=0): # A voir ici
    line = []
    for i in range(0,len(px)-1):
        lineTemp = mathLine((px[i], y, pz[i]), (px[i+1], y, pz[i+1]), 0)
        for i in lineTemp:
            line.append((i[0],i[2]))
    return(line)

def initPoints(points, type, res, num=0): # Rajouter bezier ici
    print(points, type, res, num)
    if type == 0:
        path = evaluate_bezier(points, res)
        if num == 0:
            x, z = points[:,0], points[:,2]
            px, pz = path[:,0], path[:,2]
        else:
            x, z = points[:,0], points[:,1]
            px, pz = path[:,0], path[:,1]
    if type == 1:
        px, pz = None, None
        pass # bezier
    return(px, pz)

def mathPerpendicular(N,points):
    x1,y1,x2,y2 = points[0][0],points[0][1],points[1][0],points[1][1]
    dx = x1-x2
    dy = y1-y2
    dist = sqrt(dx*dx + dy*dy)
    dx /= dist
    dy /= dist
    x3 = x1 + (N/2)*dy
    y3 = y1 - (N/2)*dx
    x4 = x1 - (N/2)*dy
    y4 = y1 + (N/2)*dx
    coorPerpendicular = round(x3),round(y3),round(x4),round(y4)
    return(coorPerpendicular)

def offset(N, listPoints):

    # 1: Calculating the perpendicular of [AB]
    coorPerpendicular0 = []
    coorPerpendicular1 = []
    for i in range(len(listPoints)-1):
        Xa, Ya, Xb, Yb = mathPerpendicular(N, (listPoints[i], listPoints[i+1]))
        coorPerpendicular0.append((Xa,Ya))
        coorPerpendicular1.append((Xb,Yb))
    
    # 2: Calculating the perpendicular of [BA]
    coorPerpendicularA = []
    coorPerpendicularB = []
    for i in range(len(listPoints)-1):
        Xa, Ya, Xb, Yb = mathPerpendicular(N, (listPoints[i+1], listPoints[i]))
        coorPerpendicularA.append((Xa,Ya))
        coorPerpendicularB.append((Xb,Yb))
    
    # 3: Adjusting the lists
    pointPerpendicularA = coorPerpendicularA.pop(0)
    pointPerpendicularB = coorPerpendicularB.pop(0)
    pointPerpendicular0 = coorPerpendicular0.pop(0)
    pointPerpendicular1 = coorPerpendicular1.pop(0)
    coorPerpendicularA.reverse()
    coorPerpendicularB.reverse()

    # 4: middle of points
    coorPerpendicularMid0 = []
    coorPerpendicularMid1 = []

    for i in range(0, len(coorPerpendicular0)):
        a,b = round((coorPerpendicularA[i][0]+coorPerpendicular1[i][0])/2), round((coorPerpendicularA[i][1]+coorPerpendicular1[i][1])/2)
        c,d = round((coorPerpendicularB[i][0]+coorPerpendicular0[i][0])/2), round((coorPerpendicularB[i][1]+coorPerpendicular0[i][1])/2)
        coorPerpendicularMid0.append((a,b))
        coorPerpendicularMid1.append((c,d))
    
    return(coorPerpendicularMid0, coorPerpendicularMid1)

#points = np.array([[3817, 100, -1742],[3816, 96, -1716],[3838, 87, -1714],[3841, 83, -1742],[3818, 80, -1742]])
#points = np.array([[3507, 118, -1830],[3532, 127, -1812],[3512, 132, -1792],[3532, 156, -1773],[3553, 137, -1768]])
points = np.array([[3399, 106, -1126],[3443, 114, -1133],[3473, 100, -1129],[3491, 109, -1131],[3502, 115, -1113],[3511, 114, -1087],[3542, 93, -1070],[3509, 69, -1041]])
#points = np.array([[3465, 70, -1306],[3441, 71, -1298],[3434, 71, -1262],[3444, 75, -1242],[3451, 78, -1230],[3463, 83, -1212],[3478, 86, -1189],[3483, 88, -1180],[3485, 88, -1143],[3486, 84, -1111],[3491, 71, -1067],[3509, 69, -1041]])
#points = np.array([[3317, 80, -1743],[3330, 85, -1717],[3315,80, -1692],[3281, 75, -1712],[3308, 80, -1726],[3340, 80, -1735],[3347, 80, -1748],[3273, 80, -1794]])
newSmoothCurve(points, 0)

#points = np.array([[3502, 1, -1715],[3551, 1, -1694],[3564, 1, -1648],[3585, 1, -1666]])
#smoothCurve(points)

#points = np.array([[3536,1, -1468],[3514, 1, -1431],[3485, 1, -1435], [3495, 1, -1460]])
#smoothCurve(points, 30)