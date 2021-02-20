def EXAMPLEsmoothCurve(points):
    # Initialisation et configuration des points
     for i in range(0,len(NombreDePoints-1)):
         # Création d'une ligne
         for i in block dans ligne:
             # Append ligne à Totale Curve
    
    # CleanLine1 : noDuplicates, pixelPerfect
    # CleanLine2 : Analyser les lignes blocks par blocks, puis, à chaque modification recommencer du début

    # Enregistrer les résultats sous forme d'une liste contenant tous les blocks dans l'ordre croissant

    for i in range(largeurDeLaRoute):
        # Calculer perpendiculaire pour chaque points de définissant les lignes

        for i in range(0,len(NombreDePoints-1)):
            # Création d'une ligne
            for i in block dans ligne:
                # Append ligne à Totale Curve
        
        # CleanLine1 : noDuplicates, pixelPerfect
        # CleanLine2 : Analyser les lignes blocks par blocks, puis, à chaque modification recommencer du début

        # Enregistrer les résultats sous forme d'une liste contenant tous les blocks dans l'ordre croissant
    
    for i in toutesLesListes:
        # poser block en fonction du numéros de la ligne, et de l'index du blocks...

def cleanLine(path):
    ''' clean and smooth a list of blocks coordinates:
    '''

    # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block
    c = 0
    while c < len(path):
        if c+3 < len(path):
            if (path[i][0] == path[i+1][0] and path[i+2][1] == path[i+3][1]):
                del path[(path[i+1])] # 2nd block
                del path[(path[i+1])] # 3rd block
                path.insert(path[i+1], (path[i+2][0],path[i+1][1]))
                continue
            elif (path[i][1] == path[i+1][1] and path[i+2][0] == path[i+3][0]):
                del path[(path[i+1])] # 2nd block
                del path[(path[i+1])] # 3rd block
                path.insert(path[i+1], (path[i+1][0],path[i+2][1]))
            else:
                c += 1 #HERE : on veut sortir de la boucle et revenir au while si il y a eu modification, et c = 0

def noDuplicates(path): #WORK
    ''' noDuplicates
    '''

    # list without duplicates
    noDuplicates = []
    for i in path:
        if i not in noDuplicates:
            noDuplicates.append(i)
    return(noDuplicates)

def pixelPerfect(path): # WORK 03/12/2020
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

    # smoothCurve
    # Créer une fonction initPoints
    # Créer une fonction line2D et qui enregistre le numéros des blocks primaires dans la liste
    # Rajouter l'option liveVisualization
    # No Duplicates
    # PixelPerfect
    # CleanLine aka smoothLine
    # = Ligne simple smooth passant par block définis
    # 3D:
    # Créer une fonction initPoints3D qui récupère la longueur de la première liste et les positions des blocks primaires
    # Faire de même : noDuplicates, pixelPerfect, smoothLine, 
    # Relier XZ avec Y
    # Return la courbe 3D

    # Faire bezierCurve au lieu de evaluate_bezier dans certain cas(arc de cercle)

    # Créer fonction parallèle
    # Prend les blocks primaires pour en déduire des perpendiculaires XZ
    # Trace les lignes
    # noDupplicates, smoothLine +pixelPerfect
    # Return les parallèles

    # Créer une fonction fill
    # Répète paralèlle

    


    
