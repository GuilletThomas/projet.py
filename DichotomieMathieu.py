import numpy
from ProjetNavireValide1 import *
import matplotlib.pyplot as plt

def Volume(fichier):
    if fichier == 'Cylindrical_HULL_Normals_Outward.stl':
        rayon = 1
        hauteur = 4
        newVolume = numpy.pi * (rayon**2) * hauteur
        return newVolume

    elif fichier == 'V_HULL_Normals_Outward.stl':
        longueur = 4
        largeur = 2
        hauteur = 1
        newVolume = longueur * largeur * hauteur
        return newVolume
    elif fichier == 'Rectangular_HULL_Normals_Outward.stl':
        longueur = 4
        largeur = 2
        hauteur = 1
        newVolume = (longueur * largeur * hauteur) /2
        return newVolume

volumeSolide = (Volume("Cylindrical_HULL_Normals_Outward.stl"))

poids = 1000 * volumeSolide

def dicho():
    listevalMilieu=[]
    za=0
    zb=1
    a=Archimede(1000, "Cylindrical_HULL_Normals_Outward.STL", za).calcul()  #Image du point x
    b=Archimede(1000, "Cylindrical_HULL_Normals_Outward.STL", zb).calcul()
    aval=a[2]-poids
    bval=b[2]-poids


    while abs(zb-za)>= 0.1 :   #Tant que les deux images ne sont pas environ = 0

        zm = (za+zb)/2        #Milieu de l'intervalle
        MilieuValeur=Archimede(1000, "Cylindrical_HULL_Normals_Outward.STL", zm).calcul() #Image de ce Milieu selon la fonction
        MilieuValeur=MilieuValeur[2]-poids

        signe = aval*MilieuValeur  #Si le signe est positif, on déplace l'intervalle car on cherche le 0 (soit là ou la fonction change de signe)

        if signe > 0:
            za = zm
            zb = zb
        if signe <0:
            za = za
            zb = zm
        a=Archimede(1000, "Cylindrical_HULL_Normals_Outward.STL", za).calcul()  #Image du point x
        b=Archimede(1000, "Cylindrical_HULL_Normals_Outward.STL", zb).calcul()
        aval=a[2]-poids
        bval=b[2]-poids
        listevalMilieu.append(MilieuValeur)
        print(za,aval,zb,bval)
    return listevalMilieu #return le x qui donne 0 en y => on a trouvé le 0 de la fonction

listevalMilieu=dicho()

print(listevalMilieu)


def Graphique(listevalMilieu):
    axs=plt.axes()
    #axs.axis([min(listeiteration)-0.2*min(listeiteration),max(listeiteration)+0.2*max(listeiteration),min(listePhi)-0.2*min(listePhi),max(listePhi)+0.2*max(listePhi)])
    plt.scatter(numpy.arange(len(listevalMilieu)),listevalMilieu, color = 'blue')
    plt.grid()
    plt.plot(numpy.arange(len(listevalMilieu)),listevalMilieu)

    plt.title('Graph')
    plt.xlabel('Itération')
    plt.ylabel('Résultante des forces N')
    plt.show()


#fig=plt.figure(figsize=(6,6))
Graphique(listevalMilieu)

#[11530.63, -3674.370000000001, 3431.629999999999, -267.3700000000008]
