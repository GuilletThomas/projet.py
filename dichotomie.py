from PousseArchimedeDiviserLesTriangles import *
import matplotlib.pyplot as plt

def dichotomie(zga, zgb, eps, poids, fichier):
    listePHI=[]
    listeIteration=[]
    iteration=0

    while abs(zgb-zga )>= eps :

        Zgm = (zga+zgb)/2

        calcularchimede = Archimede(1000, fichier, Zgm)
        liste = calcularchimede.calcul()

        signe = zga * Zgm

        if signe > 0:
            zga = Zgm
            zgb = zgb
        else:
            zga = zga
            zgb = Zgm

        PHI = abs(liste[0]) - abs(poids)
        listePHI.append(PHI)
        listeIteration.append(iteration)
        iteration+=1

        print(PHI)

    return zga, listeIteration, listePHI



poids = 200
zga = 5
zgb = 7
eps = 1*10**(-3)
fichier = 'V_HULL.stl'

newZga, listeiteration, listePHI = dichotomie(zga, zgb, eps, poids, fichier)
#print(newZga)

axs=plt.axes()
axs.axis([min(listeiteration)-0.2*min(listeiteration),max(listeiteration)+0.2*max(listeiteration),min(listePHI)-0.2*min(listePHI),max(listePHI)+0.2*max(listePHI)])
plt.scatter(listeiteration,listePHI, color = 'red')
plt.grid()
plt.plot(listeiteration,listePHI)

plt.title('Graph')
plt.xlabel('Itération')
plt.ylabel('Résultante des forces N')
plt.title("Résultante des forces au cours de la simulation")
plt.show()