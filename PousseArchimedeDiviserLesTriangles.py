"""Ici on prend en compte le bon decoupage des triangles en fonction du niveau d'eau"""
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

                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
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

                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
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

                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                sommex+=(ZFk*vectoriel1x*signe)+(ZFk*vectoriel2x*signe)
                sommey+=(ZFk*vectoriel1y*signe)+(ZFk*vectoriel2y*signe)
                sommez+=(ZFk*vectoriel1z*signe)+(ZFk*vectoriel2z*signe)

            #ici le point A et B sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau<zB and hauteureau>=zC:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'A','B',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]

                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                sommex+=(ZFk*vectoriel1x*signe)
                sommey+=(ZFk*vectoriel1y*signe)
                sommez+=(ZFk*vectoriel1z*signe)

            #ici le point B et C sommet du triangle est en dehors de l'eau
            elif hauteureau<zB and hauteureau<zC and hauteureau>=zA:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'B','C',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]

                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                sommex+=(ZFk*vectoriel1x*signe)
                sommey+=(ZFk*vectoriel1y*signe)
                sommez+=(ZFk*vectoriel1z*signe)

            #ici le point C et A sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau<zC and hauteureau>=zB:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'C','A',i)
                vectoriel1x=listesomme[0]
                vectoriel1y=listesomme[1]
                vectoriel1z=listesomme[2]

                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
                sommex+=(ZFk*vectoriel1x*signe)
                sommey+=(ZFk*vectoriel1y*signe)
                sommez+=(ZFk*vectoriel1z*signe)


            #ici le triangle est totalent sous l'eau
            elif hauteureau>=zA and hauteureau>=zB and hauteureau >=zC:
                signe=self.VerificationOriantionDuVecteurUnitaire(vectorielx,vectoriely,vectorielz,NORME)
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

        return Archimedex,Archimedey,Archimedez

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

    def TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(self,A,B,C,pointsommet,I):
        hauteureau=self.__hauteureau
        if pointsommet=='A':
            Xa=A[I][0]
            Ya=A[I][1]
            Za=A[I][2]

            Xb=B[I][0]
            Yb=B[I][1]
            Zb=B[I][2]

            Xc=C[I][0]
            Yc=C[I][1]
            Zc=C[I][2]
        elif pointsommet=='B':
            Xa=B[I][0]
            Ya=B[I][1]
            Za=B[I][2]

            Xb=C[I][0]
            Yb=C[I][1]
            Zb=C[I][2]

            Xc=A[I][0]
            Yc=A[I][1]
            Zc=A[I][2]
        elif pointsommet=='C':
            Xa=C[I][0]
            Ya=C[I][1]
            Za=C[I][2]

            Xb=A[I][0]
            Yb=A[I][1]
            Zb=A[I][2]

            Xc=B[I][0]
            Yc=B[I][1]
            Zc=B[I][2]

        #ecrire la démo!!!!
        #point E
        t1=(hauteureau-Za)/(Zb-Za)
        X1=Xa+t1*(Xb-Xa)
        Y1=Ya+t1*(Yb-Ya)

        #point D
        t2=(hauteureau-Za)/(Zc-Za)
        X2=Xa+t2*(Xc-Xa)
        Y2=Ya+t2*(Yc-Ya)

        #faire Produit vectorielle pour les 2 triangles:
        #triangle 1 avec ses trois sommets (EBC): (x,y,z)
        #E=X1,Y1,hauteureau
        #B=Xb,Yb,Zb
        #C=Xc,Yc,Zc

        #trouver le vecteur EB
        EBx=Xb-X1
        EBy=Yb-Y1
        EBz=Zb-hauteureau

        #trouver le vecteur EC
        ECx=Xc-X1
        ECy=Yc-Y1
        ECz=Zc-hauteureau

        #mes resultats du produit vectoriel et ensuite je divise par deux (voir formule poussée d'archimede)
        vectoriel1x=(EBy*ECz-EBz*ECy)/2
        vectoriel1y=(EBz*ECx-EBx*ECz)/2
        vectoriel1z=(EBx*ECy-EBy*ECx)/2


        #triangle 2 avec ses trois sommets(CDE): (x,y,z)
        #C=Xc,Yc,Zc
        #D=X2,Y2,hauteureau
        #E=X1,Y1,hauteureau

        #trouver le vecteur CE
        CEx=X1-Xc
        CEy=Y1-Yc
        CEz=hauteureau-Zc

        #trouver le vecteur CD
        CDx=X2-Xc
        CDy=Y2-Yc
        CDz=hauteureau-Zc

        #mes resultats du produit vectoriel et ensuite je divise par deux (voir formule poussée d'archimede)
        vectoriel2x=(CEy*CDz-CEz*CDy)/2
        vectoriel2y=(CEz*CDx-CEx*CDz)/2
        vectoriel2z=(CEx*CDy-CEy*CDx)/2

        return vectoriel1x,vectoriel1y,vectoriel1z,vectoriel2x,vectoriel2y,vectoriel2z

    def TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(self,A,B,C,pointsommet1,pointsommet2,I):
        hauteureau=self.__hauteureau
        if pointsommet1=='A' and pointsommet2=='B':
            Xa=C[I][0]
            Ya=C[I][1]
            Za=C[I][2]

            Xb=A[I][0]
            Yb=A[I][1]
            Zb=A[I][2]

            Xc=B[I][0]
            Yc=B[I][1]
            Zc=B[I][2]
        elif pointsommet1=='B' and pointsommet2=='C':
            Xa=A[I][0]
            Ya=A[I][1]
            Za=A[I][2]

            Xb=B[I][0]
            Yb=B[I][1]
            Zb=B[I][2]

            Xc=C[I][0]
            Yc=C[I][1]
            Zc=C[I][2]
        elif pointsommet1=='C' and pointsommet2=='A':
            Xa=B[I][0]
            Ya=B[I][1]
            Za=B[I][2]

            Xb=C[I][0]
            Yb=C[I][1]
            Zb=C[I][2]

            Xc=A[I][0]
            Yc=A[I][1]
            Zc=A[I][2]

        #point E
        t1=(hauteureau-Za)/(Zb-Za)
        X1=Xa+t1*(Xb-Xa)
        Y1=Ya+t1*(Yb-Ya)

        #point D
        t2=(hauteureau-Za)/(Zc-Za)
        X2=Xa+t2*(Xc-Xa)
        Y2=Ya+t2*(Yc-Ya)

        #triangle  avec ses trois sommets (AED): (x,y,z)
        #A=Xa,Ya,Za
        #D=X1,Y1,hauteureau
        #E=X2,Y2,hauteureau

        #trouver le vecteur AD
        ADx=X1-Xa
        ADy=Y1-Ya
        ADz=hauteureau-Za

        #trouver le vecteur AE
        AEx=X2-Xa
        AEy=Y2-Ya
        AEz=hauteureau-Za

        #mes resultats du produit vectoriel et ensuite je divise par deux (voir formule poussée d'archimede)
        vectorielx=(ADy*AEz-ADz*AEy)/2
        vectoriely=(ADz*AEx-ADx*AEz)/2
        vectorielz=(ADx*AEy-ADy*AEx)/2
        return vectorielx,vectoriely,vectorielz

#massevolumique,fichier,hauteureau
calcularchimede=Archimede(1000,'Cylindrical_HULL_Normals_Outward.stl',1)
liste=calcularchimede.calcul()
print("poussee d'archimede:")
print("x:",liste[0],"N,","y:",liste[1],'N,',"z:",liste[2],'N')
