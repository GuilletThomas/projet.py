import numpy
from OpenSTLFile import your_mesh
def Main(fichier):
    contenu=fichier.read()
    nbfacettes=CalculNbFacettes(fichier,contenu)
    print(nbfacettes)
    print(contenu)
    fichier.close()

def CalculNbFacettes(fichier,contenu):
    nbfacettes=contenu.count("facet normal") #A chaque facette définie, le compteur +=1, on obtient le nb de facettes du stl
    return nbfacettes

def GetData(fichier):
    contenu=fichier.read()
    X,Y,Z=your_mesh.v0,your_mesh.v1,your_mesh.v2
    liste=[]

    for i in range (0,len(X)):
        M=numpy.array([[X[i]],[Y[i]],[Z[i]]])
        liste.append(M)
    print(liste)

fichier=open(r"V_HULL.stl",'r')
#Main(fichier)
GetData(fichier)
#M=numpy.array([[0,-1],[1,0]])
