def cleanLine(path):
    ''' clean and smooth a list of blocks coordinates:
    '''

    
    i = 0
    while i < len(path):
        print("C")
        # 2 blocks, 90 degrees, 2 blocks = 1 block, 1 block, 1 block
        if i+3 <= len(path):
            if (path[i][0] == path[i+1][0] and path[i+2][1] == path[i+3][1]): # WORK
                path.insert((i+1), (path[i+2][0],path[i+1][1]))
                del path[i+2] # 2nd block
                del path[i+2] # 3rd block
                i = 0
                print("A")
                continue
            elif (path[i][1] == path[i+1][1] and path[i+2][0] == path[i+3][0]): # MAY WORK
                path.insert((i+1), (path[i+1][0],path[i+2][1]))
                del path[(path[i+2])] # 2nd block
                del path[(path[i+2])] # 3rd block
                i = 0
                print("B")
                continue
        
        # 1 block, 3 blocks, 1 block = 1 block, 2 blocks, 2 blocks
        if i-1 >= 0 and i+5 <= len(path):
            print("1")
            if (path[i+1][1] == path[i+2][1] and path[i+2][1] == path[i+3][1]) and \
            (path[i+1][1] != path[i][1] and path[i+3][1] != path[i+4][1]) and \
            (path[i-1][0] != path[i][0] and path[i+4][0] != path[i+5][0]):
                path.insert((i+1), (path[i+1][0],path[i][1]))
                del path[(i+2)] # 2nd block
       2")
                continue
            elif (path[i+1][0] == path[i+2][0] and path[i+2][0] == path[i+3][0]) and \
            (path[i+1][0] != path[i][0] and path[i+3][0] != path[i+4][0]) and \
            (path[i-1][1] != path[i][1] and path[i+4][1] != path[i+5][1]):
                path.insert((i+1), (path[i][0],path[i+1][1]))
                del path[(i+2)] # 2nd block
                i = 0
                print("3")         i = 0
                print("
                continue

        i += 1
    return(path)

print("start")
print(cleanLine([(-1,-1),(0,0),(1,1),(1,2),(1,3),(2,4),(3,5),(3,6),(4,7),(5,7)]))
print("end")

# solution 03/12/2020 : vérifier après modification si elles n'apportent pas d'autres erreurs, si non continuer, mis en tampon...