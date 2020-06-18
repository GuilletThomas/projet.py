import numpy
from PousseeArchimedeOfficiel import *

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
        newVolume = longueur * largeur * hauteur/2
        return newVolume
    elif fichier == 'Rectangular_HULL_Normals_Outward.stl':
        longueur = 4
        largeur = 2
        hauteur = 1
        newVolume = (longueur * largeur * hauteur)
        return newVolume


def dicho(precision,fichier,zm,masse):
    if masse==None:
        poids=1000*Volume(fichier)
    else:
        poids=masse*9.81

    listevalNiveauDeau=[] #Stock tous les niveaux d'eau jusqu'à atteindre le niveau d'équilibre
    listeCalculNiveauDeau=[] #Stock respectivement le calcul Pa-P associé à chaque niveau
    za=0 #Valeur minimum de l'eau
    zb=1 #Valeur Max de l'eau
    while zm<za or zm>zb:  #L'eau doit être comprise entre ces deux niveaux, sinon on demande un nouvel input
        print("Erreur, Le niveau d'eau doit être compris entre 0 et 1.","\nEntrez à nouveau zm")
        zm=float(input("Entrez valeur niveau d'eau en mètre >"))
    zmcalcul=Archimede(1000, fichier, zm).calcul() #Archimede renvoit les composantes X Y Z, on va donc prendre l'index 2 pour obtenir composante Z
    if zmcalcul[2]<poids:
        print("Pas d'équilibre, le bateau tend à s'enfoncer")
    elif zmcalcul[2]>poids:
        print("Pas d'équilibre, le bateau tend à sortir de l'eau")
    else :
        print("Equilibre atteint")
        return #Arret de la fonction car l'équilibre a été trouvé directement par l'utilisateur

    a=Archimede(1000, fichier, za).calcul()

    avalue=a[2]-poids

    while abs(zb-za)>= precision :   #Tant que les deux images ne sont pas environ = 0, la dichotomie continuera

        zm = (za+zb)/2        #Milieu de l'intervalle
        MilieuValeur=Archimede(1000, fichier, zm).calcul() #Image de ce Milieu selon la fonction
        MilieuValeur=MilieuValeur[2]-poids

        signe = avalue*MilieuValeur  #Selon le signe du produit des 2 images, on décale l'intervalle d'étude car on cherche le 0 (soit l'intervalle où la fonction change de signe)

        if signe > 0:
            za = zm
        if signe <0:
            zb = zm
        a=Archimede(1000, fichier, za).calcul()   #On calcule à nouveau car les points ont changé (décalage d'intervalle)

        avalue=a[2]-poids
        listevalNiveauDeau.append(zm)              #On recupere tous les niveaux d'eau
        listeCalculNiveauDeau.append(MilieuValeur) #Et leur Pa-P correspondant
    return listevalNiveauDeau,listeCalculNiveauDeau

