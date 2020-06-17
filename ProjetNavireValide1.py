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
            vectorielx=(ABy*ACz-ABz*ACy)
            vectoriely=(ABz*ACx-ABx*ACz)
            vectorielz=(ABx*ACy-ABy*ACx)
            normevectoriel=((vectorielx**2)+(vectoriely**2)+(vectorielz)**2)**(1/2)

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
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(a,b,c,'A',i,NORME)
                moncalcul1x=listesomme[0]
                moncalcul1y=listesomme[1]
                moncalcul1z=listesomme[2]
                moncalcul2x=listesomme[3]
                moncalcul2y=listesomme[4]
                moncalcul2z=listesomme[5]

                sommex+=(moncalcul1x)+(moncalcul2x)
                sommey+=(moncalcul1y)+(moncalcul2y)
                sommez+=(moncalcul1z)+(moncalcul2z)

            #ici le point B sommet du triangle est en dehors de l'eau
            elif hauteureau<zB and hauteureau>=zA and hauteureau>=zC:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(a,b,c,'B',i,NORME)
                moncalcul1x=listesomme[0]
                moncalcul1y=listesomme[1]
                moncalcul1z=listesomme[2]
                moncalcul2x=listesomme[3]
                moncalcul2y=listesomme[4]
                moncalcul2z=listesomme[5]

                sommex+=(moncalcul1x)+(moncalcul2x)
                sommey+=(moncalcul1y)+(moncalcul2y)
                sommez+=(moncalcul1z)+(moncalcul2z)

            #ici le point C sommet du triangle est en dehors de l'eau
            elif hauteureau<zC and hauteureau>=zB and hauteureau>=zA:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(a,b,c,'C',i,NORME)
                moncalcul1x=listesomme[0]
                moncalcul1y=listesomme[1]
                moncalcul1z=listesomme[2]
                moncalcul2x=listesomme[3]
                moncalcul2y=listesomme[4]
                moncalcul2z=listesomme[5]

                sommex+=(moncalcul1x)+(moncalcul2x)
                sommey+=(moncalcul1y)+(moncalcul2y)
                sommez+=(moncalcul1z)+(moncalcul2z)

            #ici le point A et B sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau<zB and hauteureau>=zC:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'A','B',i,NORME)
                moncalculx=listesomme[0]
                moncalculy=listesomme[1]
                moncalculz=listesomme[2]

                sommex+=moncalculx
                sommey+=moncalculy
                sommez+=moncalculz

            #ici le point B et C sommet du triangle est en dehors de l'eau
            elif hauteureau<zB and hauteureau<zC and hauteureau>=zA:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'B','C',i,NORME)
                moncalculx=listesomme[0]
                moncalculy=listesomme[1]
                moncalculz=listesomme[2]

                sommex+=moncalculx
                sommey+=moncalculy
                sommez+=moncalculz
            #ici le point C et A sommet du triangle est en dehors de l'eau
            elif hauteureau<zA and hauteureau<zC and hauteureau>=zB:
                listesomme=self.TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(a,b,c,'C','A',i,NORME)
                moncalculx=listesomme[0]
                moncalculy=listesomme[1]
                moncalculz=listesomme[2]

                sommex+=moncalculx
                sommey+=moncalculy
                sommez+=moncalculz


            #ici le triangle est totalent sous l'eau
            elif hauteureau>=zA and hauteureau>=zB and hauteureau >=zC:
                sommex+=(ZFk*0.5*normevectoriel*NORME[0])
                sommey+=(ZFk*0.5*normevectoriel*NORME[1])
                sommez+=(ZFk*0.5*normevectoriel*NORME[2])


        """
        PARTIE 4 : calcul final Poussée d'archimede
        """
        #on applique la formule du Cumul sur l’ensemble des facettes immergées par la poussée d’Arichimède
        Archimedex=int(massevolumique*gravite*sommex)
        Archimedey=int(massevolumique*gravite*sommey)
        Archimedez=int(massevolumique*gravite*sommez)

        return Archimedex,Archimedey,Archimedez,compteur


    def TrouvecoordonneePourCouperLeTriangleAvecUnSommetDehors(self,A,B,C,pointsommet,I,Norme):
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
        X2=Xa+t2 *(Xc-Xa)
        Y2=Ya+t2*(Yc-Ya)

        #faire Produit vectorielle pour les 2 triangles:
        #triangle 1 avec ses trois sommets (EBC): (x,y,z)
        #E=X1,Y1,hauteureau
        #B=Xb,Yb,Zb
        #C=Xc,Yc,Zc
        centregraviteGzEBC=(hauteureau+Zb+Zc)/3
        ZFkEBC=centregraviteGzEBC-hauteureau

        #trouver le vecteur EB
        EBx=Xb-X1
        EBy=Yb-Y1
        EBz=Zb-hauteureau

        #trouver le vecteur EC
        ECx=Xc-X1
        ECy=Yc-Y1
        ECz=Zc-hauteureau

        #mes resultats du produit vectoriel (voir formule poussée d'archimede) EB^EC
        vectoriel1x=((EBy*ECz-EBz*ECy))
        vectoriel1y=((EBz*ECx-EBx*ECz))
        vectoriel1z=((EBx*ECy-EBy*ECx))

        lanormex=Norme[0]
        lanormey=Norme[1]
        lanormez=Norme[2]

        normevectoriel1=((vectoriel1x**2)+(vectoriel1y**2)+(vectoriel1z)**2)**(1/2)

        resultat1x=normevectoriel1*(0.5)*lanormex*ZFkEBC
        resultat1y=normevectoriel1*(0.5)*lanormey*ZFkEBC
        resultat1z=normevectoriel1*(0.5)*lanormez*ZFkEBC


        #triangle 2 avec ses trois sommets(CDE): (x,y,z)
        #C=Xc,Yc,Zc
        #D=X2,Y2,hauteureau
        #E=X1,Y1,hauteureau
        centregraviteGzCDE=(hauteureau+hauteureau+Zc)/3
        ZFkCDE=centregraviteGzCDE-hauteureau

        #trouver le vecteur CE
        CEx=X1-Xc
        CEy=Y1-Yc
        CEz=hauteureau-Zc

        #trouver le vecteur CD
        CDx=X2-Xc
        CDy=Y2-Yc
        CDz=hauteureau-Zc

        #mes resultats du produit vectoriel  (voir formule poussée d'archimede) CE^CD
        vectoriel2x=((CEy*CDz-CEz*CDy))
        vectoriel2y=((CEz*CDx-CEx*CDz))
        vectoriel2z=((CEx*CDy-CEy*CDx))

        normevectoriel2=((vectoriel2x**2)+(vectoriel2y**2)+(vectoriel2z)**2)**(1/2)

        resultat2x=normevectoriel2*(0.5)*lanormex*ZFkCDE
        resultat2y=normevectoriel2*(0.5)*lanormey*ZFkCDE
        resultat2z=normevectoriel2*(0.5)*lanormez*ZFkCDE

        return resultat1x,resultat1y,resultat1z,resultat2x,resultat2y,resultat2z

    def TrouvecoordonneePourCouperLeTriangleAvecDeuxSommetsDehors(self,A,B,C,pointsommet1,pointsommet2,I,Norme):
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
        centregraviteGzAED=(Za+hauteureau+hauteureau)/3
        ZFkAED=centregraviteGzAED-hauteureau

        #trouver le vecteur AD
        ADx=X1-Xa
        ADy=Y1-Ya
        ADz=hauteureau-Za

        #trouver le vecteur AE
        AEx=X2-Xa
        AEy=Y2-Ya
        AEz=hauteureau-Za

        lanormex=Norme[0]
        lanormey=Norme[1]
        lanormez=Norme[2]

        #mes resultats du produit vectoriel et ensuite je divise par deux (voir formule poussée d'archimede)
        vectorielx=((ADy*AEz-ADz*AEy))
        vectoriely=((ADz*AEx-ADx*AEz))
        vectorielz=((ADx*AEy-ADy*AEx))

        normevectoriel=((vectorielx**2)+(vectoriely**2)+(vectorielz)**2)**(1/2)

        resultatx=normevectoriel*(0.5)*lanormex*ZFkAED
        resultaty=normevectoriel*(0.5)*lanormey*ZFkAED
        resultatz=normevectoriel*(0.5)*lanormez*ZFkAED


        return resultatx,resultaty,resultatz

#massevolumique,fichier,hauteureau
calcularchimede=Archimede(1000,'V_HULL_Normals_Outward.STL',0.5)
liste=calcularchimede.calcul()
print("poussee d'archimede:")
print("x:",liste[0],"N,","y:",liste[1],'N,',"z:",liste[2],'N')

"""Ici on prend en compte le bon decoupage des triangles en fonction du niveau d'eau sans test de la norme"""
