class block:
    def __init__(self, id, coords):
        self.id = id
        self.coords = coords
    
b1 = block("minecraft:dirt", (36, 5, 33))

print(b1.id, b1.coords)

'''
créer une classe pour gérer les blocks, une autre pour les courbes...
'''

class curve:
    def __init__(self, points):
        # Calculer la courbe passant par points, puis enregistrer les blocks sous formes d'objets avec voisins

        # A partir des objets, calculer s'ils doivent être détruits ou pas en fonction de leur voisins. EDIT : peut-être pas, trop compliqué pour une ligne. Mais peut-être utilie pour une route