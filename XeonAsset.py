#XeonAsset.py made by Xeon0X and REXOS for GDMC

from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from math import *

inputs = [
    (
        ("setBlock", "title"),
        ("Block", 1),
        ("Data", 0),
        ("x", 0),
        ("y", 0),
        ("z", 0),
        ("Run setBlock", False)
    ),

    (
        ("setLine", "title"),
        ("Block1", 1),
        ("Data1", 0),
        ("x1", 0),
        ("y1", 0),
        ("z1", 0),
        ("x2", 0),
        ("y2", 0),
        ("z2", 0),
        ("Run setLine", False)
    )
]

def perform(level, box, options):

    def setBlock(level, (block, data), (x, y, z)):
        level.setBlockAt((int)(x),(int)(y),(int)(z), block)
        level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)

    # With setBlock, mathLine
    def setLine((block1, data1), (x1, y1, z1), (x2, y2, z2)):
        points = mathLine((x1, y1, z1), (x2, y2, z2))

        for i in points:
                setBlock(level, (block1, data1), (i[0], i[1], i[2]))

    # With mathBeizer, setLine
    def setBezier((block, data), n,x,y, y0):
        coorBezier = mathBezier(n,x,y)
        d = 0 # For debug
        for i in range(0,(len(coorBezier)-1)):
            if d < 17:
                setBlock(level, (35, d), (coorBezier[i][0], y0+1, coorBezier[i][1])) # For debug
                d += 1 # For debug
            else : 
                d = 0 # For debug
            setLine((block, data), (coorBezier[i][0], y0, coorBezier[i][1]), (coorBezier[i+1][0], y0, coorBezier[i+1][1]))

    # Ici -------------------------------
    def setBezierOffset((block, data), n,x,y, y0, N):
        setBezier((block, data), n,x,y, y0)
        coorBezier = mathBezier(n,x,y)
        coorPerpendicular = []
        coorVerificationSecants = []

        for i in range(0,(len(coorBezier)-1)):
            ''' Module calculant toutes les coordonnees perpendiculaires
                et les enregistrant avec leur point respectif 
            '''
            Xa,Ya,Xb,Yb = mathPerpendicular(N,(coorBezier[i][0],coorBezier[i][1]),(coorBezier[i+1][0],coorBezier[i+1][1]))
            coor = Xa,Ya,Xb,Yb,coorBezier[i][0],coorBezier[i][1]
            X1,Y1,X2,Y2 = mathPerpendicular(N,(coorBezier[i+1][0],coorBezier[i+1][1]),(coorBezier[i][0],coorBezier[i][1]))
            coor1 = X2,Y2,X1,Y1,coorBezier[i+1][0],coorBezier[i+1][1]
            coorVerificationSecants.append(coor)
            coorVerificationSecants.append(coor1)
        
        for i in range(0,(len(coorVerificationSecants))):
            ''' Verifie pour chaque point perpendiculaire s'ils sont a l'exterieur du rayon choisi de chaque point
                puis l'ajoute dans ce cas a la liste des points utilisable
            '''
            coorAppend = 0
            for j in range(0,(len(coorBezier))):
                InRadius = mathInRadius(coorBezier[j][0],coorBezier[j][1],coorVerificationSecants[i][0],coorVerificationSecants[i][1],(N/2)-1)
                if InRadius == True:
                    coorAppend += 1
                    print(j,i)
            if coorAppend == 0:
                coorPerpendicular.append(coorVerificationSecants[i])

        for i in range(0,(len(coorPerpendicular)-1)):
            setLine((block, data), (coorPerpendicular[i][0], y0, coorPerpendicular[i][1]), (coorPerpendicular[i+1][0], y0, coorPerpendicular[i+1][1]))
            
    # For setLine (Python3 code for generating points on a 3-D line using Bresenham's Algorithm)
    def mathLine((x1, y1, z1), (x2, y2, z2)): 
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
                if (p1 >= 0): 
                    y1 += ys 
                    p1 -= 2 * dx 
                if (p2 >= 0): 
                    z1 += zs 
                    p2 -= 2 * dx 
                p1 += 2 * dy 
                p2 += 2 * dz 
                ListOfPoints.append((x1, y1, z1)) 
    
        # Driving axis is Y-axis" 
        elif (dy >= dx and dy >= dz):        
            p1 = 2 * dx - dy 
            p2 = 2 * dz - dy 
            while (y1 != y2): 
                y1 += ys 
                if (p1 >= 0): 
                    x1 += xs 
                    p1 -= 2 * dy 
                if (p2 >= 0): 
                    z1 += zs 
                    p2 -= 2 * dy 
                p1 += 2 * dx 
                p2 += 2 * dz 
                ListOfPoints.append((x1, y1, z1)) 
    
        # Driving axis is Z-axis" 
        else:         
            p1 = 2 * dy - dz 
            p2 = 2 * dx - dz 
            while (z1 != z2): 
                z1 += zs 
                if (p1 >= 0): 
                    y1 += ys 
                    p1 -= 2 * dz 
                if (p2 >= 0): 
                    x1 += xs 
                    p2 -= 2 * dz 
                p1 += 2 * dy 
                p2 += 2 * dx 
                ListOfPoints.append((x1, y1, z1)) 
        return ListOfPoints

    # For mathBezier
    def mathBezierAsset(coorArr, i, j, t):
        if j == 0:
            return coorArr[i]
        return mathBezierAsset(coorArr, i, j - 1, t) * (1 - t) + mathBezierAsset(coorArr, i + 1, j - 1, t) * t

    # With mathBezierAsset, for setBezier, using deCastlejau algorithm
    def mathBezier(n,x,y):
        coorArrX = []
        coorArrY = []
        coorBezier = []
        coorOffset = []

        for i in range(0,len(x)):
            coorArrX.append(x[i])
            coorArrY.append(y[i])

        # Plot the curve
        numSteps = 25
        for k in range(numSteps):
            t = float(k) / (numSteps - 1)
            x = int(mathBezierAsset(coorArrX, 0, n - 1, t))
            y = int(mathBezierAsset(coorArrY, 0, n - 1, t))
            try:
                coorXY = x,y
                coorBezier.append(coorXY)
            except:
                pass

        return coorBezier

    def mathPerpendicular(N,(x1,y1),(x2,y2)):
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

    def mathInRadius(center_x, center_y, x, y, radius):
        dist = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
        if dist <= radius:
            return True
        else :
            return False

    # Interface

    block = options["Block"]
    data = options["Data"]
    block1 = options["Block1"]
    data1 = options["Data1"]
    x = options["x"]
    y = options["y"]
    z = options["z"]
    x1 = options["x1"]
    y1 = options["y1"]
    z1 = options["z1"]
    x2 = options["x2"]
    y2 = options["y2"]
    z2 = options["z2"]

    if options["Run setBlock"] == True:
        setBlock(level, (block, data), (x, y, z))
    if options["Run setLine"] == True:
        setLine((block1, data1), (x1, y1, z1), (x2, y2, z2))

    #setBezier(1, 0, 3,(-15,-15,20),(-15,15,15), 7)
    #test = (mathPerpendicular(40,(-80,40),(-95,-13)))
    #setLine((57, 0), (-80, 20, 40), (-95, 20, -13))
    #setLine((57, 0), (test[0], 20, test[1]), (test[2], 20, test[3]))
    setBezierOffset((35, 0), 5,(-7,-60,-70,-120,-30),(30,50,15,7,-20), 175, 2)
    setBezierOffset((35, 1), 5,(-7,-60,-70,-120,-30),(30,50,15,7,-20), 175, 4)
    setBezierOffset((35, 2), 5,(-7,-60,-70,-120,-30),(30,50,15,7,-20), 175, 6)
    setBezierOffset((35, 3), 5,(-7,-60,-70,-120,-30),(30,50,15,7,-20), 175, 8)
    setBezierOffset((35, 4), 5,(-7,-60,-70,-120,-30),(30,50,15,7,-20), 175, 10)