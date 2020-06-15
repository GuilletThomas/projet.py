"""Ici on suppose que l'objet est totalement immergé """
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
"source: https://readthedocs.org/projects/numpy-stl/downloads/pdf/latest/"

class Archimede:
    def __init__(self,massevolumique,fichier,hauteureau):
        self.__massevolumique=massevolumique
        self.__fichier=fichier
        self.__hauteureau=hauteureau
    def calcul(self):
        sommex=0
        sommey=0
        sommez=0
        gravite=9.81
        massevolumique=self.__massevolumique
        hauteureau=self.__hauteureau

        #overture de mon fichier
        monfichier=self.__fichier
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)
        your_mesh = mesh.Mesh.from_file(monfichier)
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

        normal=your_mesh.normals
        #obtenir les trois coordonnées x,y,z des trois sommets du triangle
        a,b,c=your_mesh.v0, your_mesh.v1, your_mesh.v2
        nombredetriangle=len(a)

        for i in range(0,nombredetriangle):
            """
            A=a[i] #le i ème point A avec 3 coordonees x,y,z
            B=b[i] #le i ème point B avec 3 coordonees x,y,z
            C=c[i] #le i ème point C avec 3 coordonees x,y,z
            """
            centredegraviteGz=(a[i][2]+b[i][2]+c[i][2])/3
            ZFk=centredegraviteGz-hauteureau

            #DSFk* nFk=(AB^AC)/2
            ABx=b[i][0]-a[i][0]
            ABy=b[i][1]-a[i][1]
            ABz=b[i][2]-a[i][2]

            ACx=c[i][0]-a[i][0]
            ACy=c[i][1]-a[i][1]
            ACz=c[i][2]-a[i][2]

            scalairex=(ABy*ACz-ABz*ACy)/2
            scalairey=(ABz*ACx-ABx*ACz)/2
            scalairez=(ABx*ACy-ABy*ACx)/2

            sommex+=(ZFk*scalairex)
            sommey+=(ZFk*scalairey)
            sommez+=(ZFk*scalairez)

        #on applique la formule du Cumul sur l’ensemble des facettes immergées par la poussée d’Arichimède
        Archimedex=int(massevolumique*gravite*sommex)
        Archimedey=int(massevolumique*gravite*sommey)
        Archimedez=int(massevolumique*gravite*sommez)

        return Archimedex,Archimedey,Archimedez


#massevolumique,fichier,hauteureau
calcularchimede=Archimede(860,'Cylindrical_HULL.stl',3)
liste=calcularchimede.calcul()
print("poussee d'archimede:")
print("x:",liste[0],",","y:",liste[1],',',"z:",liste[2])