"""Ici on prend en compte le bon decoupage des triangles en fonction du niveau d'eau sans test de la norme"""
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
#"source: https://readthedocs.org/projects/numpy-stl/downloads/pdf/latest/"

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
        compteur=0


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

        #on parcourt notre fichier STL
        for i in range(0,nombredetriangle):
            """
            PARTIE 1 : centre de gravité et calcul de ZFk
            """
            """
            A=a[i] #le i ème point A avec 3 coordonees x,y,z
            B=b[i] #le i ème point B avec 3 coordonees x,y,z
            C=c[i] #le i ème point C avec 3 coordonees x,y,z
            """
            centredegraviteGz=(a[i][2]+b[i][2]+c[i][2])/3
            ZFk=centredegraviteGz-hauteureau

            """
            PARTIE 2 : calcul du produit vectoriel
            """
            zA=a[i][2] #on prend la hauteur z du point A
            zB=b[i][2] #on prend la hauteur z du point B
            zC=c[i][2] #on prend la hauteur z du point C

            #calcul du produit vectoriel
            #DSFk* nFk=(AB^AC)/2

            #trouver le vecteur AB
            ABx=b[i][0]-a[i][0]
            ABy=b[i][1]-a[i][1]
            ABz=b[i][2]-a[i][2]

            #trouver le vecteur AC
            ACx=c[i][0]-a[i][0]
            ACy=c[i][1]-a[i][1]
            ACz=c[i][2]-a[i][2]

            #mes resultats du produit vectoriel et ensuite je divise par deux (voir formule poussée d'archimede
            vectorielx=(ABy*ACz-ABz*ACy)/2
            vectoriely=(ABz*ACx-ABx*ACz)/2
            vectorielz=(ABx*ACy-ABy*ACx)/2


            #la norme
            NORME=normal[i]

            #permet de couper correctement les triangles pour la poussée d'archimede:

            #ici le triangle est strciteemnt en dehors de l'eau donc la poussée d'archimede vaut 0
            if hauteureau< zA and hauteureau< zB and hauteureau< zC:
                sommex=sommex
                sommey=sommey
                sommez=sommez

            #ici le point A sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau>=zB and hauteureau>=zC:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(a,b,c,'A',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]
                vectoriel2x=listesomme[3]
                vectoriel2y=listesomme[4]
                vectoriel2z=listesomme[5]

                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectoriel1x*signe)+(ZFk*vectoriel2x*signe)
                sommey+=(ZFk*vectoriel1y*signe)+(ZFk*vectoriel2y*signe)
                sommez+=(ZFk*vectoriel1z*signe)+(ZFk*vectoriel2z*signe)

            #ici le point B sommet du triangle est en dehors de l'eau
            elif hauteureau<zB and hauteureau>=zA and hauteureau>=zC:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(a,b,c,'B',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]
                vectoriel2x=listesomme[3]
                vectoriel2y=listesomme[4]
                vectoriel2z=listesomme[5]

                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectoriel1x*signe)+(ZFk*vectoriel2x*signe)
                sommey+=(ZFk*vectoriel1y*signe)+(ZFk*vectoriel2y*signe)
                sommez+=(ZFk*vectoriel1z*signe)+(ZFk*vectoriel2z*signe)

            #ici le point C sommet du triangle est en dehors de l'eau
            elif hauteureau<zC and hauteureau>=zB and hauteureau>=zA:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(a,b,c,'C',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]
                vectoriel2x=listesomme[3]
                vectoriel2y=listesomme[4]
                vectoriel2z=listesomme[5]

                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectoriel1x*signe)+(ZFk*vectoriel2x*signe)
                sommey+=(ZFk*vectoriel1y*signe)+(ZFk*vectoriel2y*signe)
                sommez+=(ZFk*vectoriel1z*signe)+(ZFk*vectoriel2z*signe)

            #ici le point A et B sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau<zB and hauteureau>=zC:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'A','B',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]

                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectoriel1x*signe)
                sommey+=(ZFk*vectoriel1y*signe)
                sommez+=(ZFk*vectoriel1z*signe)

            #ici le point B et C sommet du triangle est en dehors de l'eau
            elif hauteureau<zB and hauteureau<zC and hauteureau>=zA:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'B','C',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]

                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectoriel1x*signe)
                sommey+=(ZFk*vectoriel1y*signe)
                sommez+=(ZFk*vectoriel1z*signe)

            #ici le point C et A sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau<zC and hauteureau>=zB:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'C','A',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]

                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectoriel1x*signe)
                sommey+=(ZFk*vectoriel1y*signe)
                sommez+=(ZFk*vectoriel1z*signe)


            #ici le triangle est totalent sous l'eau
            elif hauteureau>=zA and hauteureau>=zB and hauteureau >=zC:
                #signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                signe=1
                sommex+=(ZFk*vectorielx*signe)
                sommey+=(ZFk*vectoriely*signe)
                sommez+=(ZFk*vectorielz*signe)

        """
        PARTIE 4 : calcul final Poussée d'archimede
        """
        #on applique la formule du Cumul sur l’ensemble des facettes immergées par la poussée d’Arichimède
        Archimedex=int(massevolumique*gravite*sommex)
        Archimedey=int(massevolumique*gravite*sommey)
        Archimedez=int(massevolumique*gravite*sommez)

        return Archimedex,Archimedey,Archimedez,compteur
    """
    def VerificationOriantionDuVecteurUnitaire(self,Vectx,Vecty,Vectz,norme):
        #étape de verification:
        # U/||U||  + V(vecteur unitaire du fichier)
        #si le resultat est different de 0 alors *(-1) pour mon produit scalaire
        normeproduitvectoriel=((Vectx**2)+(Vecty**2)+(Vectz**2))**(1/2) #vecteur unitaire du triangle

        MonVexteuruniformex=Vectx/normeproduitvectoriel
        MonVexteuruniformey=Vecty/normeproduitvectoriel
        MonVexteuruniformez=Vectz/normeproduitvectoriel

        vecteurunitairedufichierX=norme[0]
        vecteurunitairedufichierY=norme[1]
        vecteurunitairedufichierZ=norme[2]

        additionDesDeuxVecteursUnitaireX=MonVexteuruniformex+vecteurunitairedufichierX
        additionDesDeuxVecteursUnitaireY=MonVexteuruniformey+vecteurunitairedufichierY
        additionDesDeuxVecteursUnitaireZ=MonVexteuruniformez+vecteurunitairedufichierZ

        signeVerification=1
        if additionDesDeuxVecteursUnitaireX!=0 and additionDesDeuxVecteursUnitaireY!=0 and additionDesDeuxVecteursUnitaireZ!=0:
            signeVerification=-1

        return signeVerification
    """




calcularchimede=Archimede(1000,'V_HULL_Normals_Outward.STL',2)
liste=calcularchimede.calcul()
print("poussee d'archimede:")
print("x:",liste[0],"N,","y:",liste[1],'N,',"z:",liste[2],'N')