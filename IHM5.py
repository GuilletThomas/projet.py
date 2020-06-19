from PySide2.QtWidgets import *
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d
from DichotomyOfficiel import *
from mpl_toolkits.mplot3d import axes3d, Axes3D #car erreur "unknown projection '3d'"
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PySide2.QtGui import *
#pour l'utilsation de Axes3D --> source "https://stackoverflow.com/questions/3810865/matplotlib-unknown-projection-3d-error"

class Test(QWidget):
    def __init__(self,fichier=None,zb=None):
        self.__fichier=fichier
        self.__zb=zb
        QWidget.__init__(self)
        self.fig = plt.figure()

        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title("Model Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        self.canvas = FigureCanvas(self.fig)
        #rafraichissement
        self.canvas.draw()

        self.setWindowTitle("Boat Calculator")
        self.setWindowIcon(QIcon('Icon.png'))
        self.layout = QGridLayout()
        self.setMinimumSize(900, 500)

        self.button1 = QPushButton("Load 3D Model")
        self.buttonfilename = QPushButton("No model currently selected")
        self.button3 = QPushButton("Compute")
        self.label1=QLabel("Initial water level (m)")
        self.label2=QLabel("Accuracy for the final water level (m)")
        self.label3=QLabel("Enter the mass of the solid (kg). (If Blank, will be by default the mass of water's volume moved)")
        self.label = QTextEdit("Calculations will be displayed here. Load your model by clicking the Load 3D Model Button, enter your data into the Intial water level and Accuracy boxes, then click on Compute."+"\n Water level value must be between 0m and the solid height. Accuracy must be positive")
        self.label11 = QLineEdit()
        self.label22 = QLineEdit()
        self.label33=QLineEdit()

        self.fig2d=plt.figure()
        self.canvas2d=FigureCanvas(self.fig2d)
        self.ax2=plt.axes()
        self.ax2.grid()
        self.ax2.set_title("Net force for several water levels by number of iterations")
        self.ax2.set_ylabel('Net force (N)')
        #self.ax2.set_title("Pa(zi)-Weight with several water levels zi obtained by dichotomy by number of iterations")
        self.canvas2d.draw()
#######Niveau eau Graph ######
        self.figniveaueau=plt.figure()
        self.canvasniveaueau=FigureCanvas(self.figniveaueau)
        self.ax3=plt.axes()
        self.ax3.grid()
        self.ax3.set_title("Water level by number of iterations")
        self.ax3.set_ylabel('Water level (m)')
        self.canvasniveaueau.draw()
        self.SaveButton = QPushButton("Save Graphs")
####
        self.layout.addWidget(self.button1, 1, 1, 1, 2)
        self.layout.addWidget(self.buttonfilename, 1, 3, 1, 2)
        self.layout.addWidget(self.button3, 1, 5, 1, 2)

        self.layout.addWidget(self.canvas2d, 4, 5, 1, 2)
        self.layout.addWidget(self.canvasniveaueau,5,5,1,2)

        self.layout.addWidget(self.canvas,3,1,4,4)
        self.layout.addWidget(self.label, 3, 5, 1, 2)
        self.layout.addWidget(self.label1,2,1,1,1)
        self.layout.addWidget(self.label11,2,2,1,1)

        self.layout.addWidget(self.label2,2,3,1,1)
        self.layout.addWidget(self.label22,2,4,1,1)

        self.layout.addWidget(self.label3,2,5,1,1)
        self.layout.addWidget(self.label33,2,6,1,1)
        self.layout.addWidget(self.SaveButton,6,6,1,1)

        self.button1.clicked.connect(self.clic)
        self.button3.clicked.connect(self.cliccompute)
        self.SaveButton.clicked.connect(self.save)
        self.setLayout(self.layout)

    def clic(self): #Afficher le Menu du Load Image
        win2.show()
    def cliccompute(self):         #On verifie la cohérence des données entrées
        if self.__fichier!=None:
            if self.label11.text()=="" and self.label22.text()=="":
                self.label11.setText("Must be completed")
                self.label22.setText("Must be completed")
            elif self.label11.text()=="" and self.label22.text()!="":
                self.label11.setText("Must be completed")
            elif self.label11.text()!="" and self.label22.text()=="":
                self.label22.setText("Must be completed")
            else :
                NiveauDeau=float(self.label11.text())
                Precision=float(self.label22.text())
                if NiveauDeau<0 or NiveauDeau>self.__zb:  #L'eau doit être comprise entre ces deux niveaux, sinon on demande un nouvel input
                    self.label11.setText("Must be between 0 and "+str(self.__zb)+" m")
                if Precision<0:
                    self.label22.setText("Must be >0")
                else:
                    self.cliccompute2()    #Si ces données sont bonnes on lance la suite du programme
        else :
            self.notif("Please load a 3D Model before")
    def cliccompute2(self):
        if self.__fichier!=None:
            Precision=float(self.label22.text())
            NiveauDeau=float(self.label11.text())
            if self.label33.text()!='':
                masse=float(self.label33.text())
            else:
                masse=None
            #fichier=str(self.__fichier)
            listevalNiveauDeau,listeCalculNiveauDeau,chaine,poids=dicho(Precision,self.__fichier,NiveauDeau,masse,self.__zb)
            self.ax2.plot(np.arange(1,len(listeCalculNiveauDeau)+1),listeCalculNiveauDeau) #On génère le graphique de la résultante des forces en fonction du nb d'itération
            self.ax2.scatter(np.arange(1,len(listeCalculNiveauDeau)+1),listeCalculNiveauDeau, color = 'blue')
            self.canvas2d.draw()
            NiveauDeauArrondi=int(listevalNiveauDeau[-1]*10**3)*10**-3  #Pour arrondir la valeur du niveau d'eau, car beaucoup de chiffres significatifs dus à la dichotomie
            self.ax3.bar(np.arange(1,len(listevalNiveauDeau)+1),listevalNiveauDeau,width=0.1) #On génère le graphique des niveaux d'eau calculés au cours de la dichotomie en fonction du nb d'itération
            self.canvasniveaueau.draw()
            self.label.setText("For a weight of "+str(poids)+" N, "+chaine+". The water level to reach the equilibrium state with an accuracy of "+ str(Precision) +" m is "+str(NiveauDeauArrondi)+"m. For this level z, the Net force is equal to Pa(z)-P="+str(listeCalculNiveauDeau[1])+" N")
            #self.Update3D()
            #Fonction Update 3D, idée qui permettrait de colorier différemment les parties du bateau en dehors et sous l'eau
    """
    def Update3D(self): 
        ax = Axes3D(self.fig)
        your_mesh = mesh.Mesh.from_file(self.__fichier)
        print(your_mesh)
        print(your_mesh.vectors)
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors,facecolors='grey'))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        """
    def save(self):   #Permet de sauvegarder les graphs sur clique du bouton Save Graphs
        if self.__fichier!=None:
            self.fig.savefig(self.__fichier+"3D_Visualization.png")
            self.fig2d.savefig(self.__fichier+"Net_Force.png")
            self.figniveaueau.savefig(self.__fichier+"Water_Level.png")
            self.notif("Graphs successfully saved")
        else:
            self.notif("You can not save empty graphs")
    def notif(self,text):
            self.Notif=QMessageBox()
            self.Notif.setWindowTitle("Info") ##########
            self.Notif.setText(text)
            self.Notif.exec_()

    def dessin(self): #Code des fonctions dessinX à optimiser. #Permet de charger le STL 3D respectif à celui choisi
        file="V"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)

        #dessin 3d
        your_mesh = mesh.Mesh.from_file('V_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)

        self.canvas.draw()
        fichiername='V_HULL_Normals_Outward.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=1


    def dessin2(self):
        file="Rectangular"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Rectangular_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='Rectangular_HULL_Normals_Outward.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=1
    def dessin3(self):
        file="Cylindrical"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Cylindrical_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='Cylindrical_HULL_Normals_Outward.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=2
    def dessin4(self):
        file="Mini650"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Mini650_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='Mini650_HULL_Normals_Outward.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=0.8
    def dessin5(self):
        file="Wigley"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('WIGLEY_L=2500_B=250_T=156_NormalOutward2.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='WIGLEY_L=2500_B=250_T=156_NormalOutward2.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=400
    def dessin6(self):
        file="Submarine"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('ssmarin_L=4_W=2_H=2_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='ssmarin_L=4_W=2_H=2_Normals_Outward.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=2
    def dessin7(self):
        file="Barge"
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        ax.set_title(file+" Visualization",fontweight='bold',fontsize=14)
        ax.set_xlabel("X",fontweight='bold',fontsize=14)
        ax.set_ylabel("Y",fontweight='bold',fontsize=14)
        ax.set_zlabel("Z",fontweight='bold',fontsize=14)
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('BargeAlu_L_2980_W_633_H_400_NormalOutward2.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='BargeAlu_L_2980_W_633_H_400_NormalOutward2.STL'
        self.__fichier=str(fichiername)
        self.buttonfilename.setText(file)
        self.__zb=400
class ButtonsPanel(QWidget):                 #Interface Menu du Load Image, on choisit le 3D Model
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Model Choice")
        self.setWindowIcon(QIcon('Icon.png'))
        self.layout = QHBoxLayout()
        self.Button=QPushButton("V")
        self.Button2=QPushButton("Rectangular")
        self.Button3=QPushButton("Cylindrical")
        self.Button4=QPushButton("Mini650")
        self.Button5=QPushButton("Wigley")
        self.Button6=QPushButton("Submarine")
        self.Button7=QPushButton("BargeAlu")
        self.label=QLabel("Choose a Model")
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.Button)
        self.layout.addWidget(self.Button2)
        self.layout.addWidget(self.Button3)
        self.layout.addWidget(self.Button4)
        self.layout.addWidget(self.Button5)
        self.layout.addWidget(self.Button6)
        self.layout.addWidget(self.Button7)
        self.setLayout(self.layout)
        self.Button.clicked.connect(self.interface1)
        self.Button2.clicked.connect(self.interface2)
        self.Button3.clicked.connect(self.interface3)
        self.Button4.clicked.connect(self.interface4)
        self.Button5.clicked.connect(self.interface5)
        self.Button6.clicked.connect(self.interface6)
        self.Button7.clicked.connect(self.interface7)
    def confirm(self,text):                                 #Confirmer l'interface chargée
        self.Notif=QMessageBox()
        self.Notif.setWindowTitle("Info") ##########
        self.Notif.setText(text)
        self.Notif.exec_()

    def interface1(self):                        #Si on Load l'interface 1, => fonction dessin qui ouvrira le STL + fonction confirm qui envoie une notification de confirmation
        win.dessin()
        self.confirm("Interface successfully loaded")
        win2.close()
    def interface2(self):
        win.dessin2()
        self.confirm("Interface successfully loaded")
        win2.close()

    def interface3(self):
        win.dessin3()
        self.confirm("Interface successfully loaded")
        win2.close()
    def interface4(self):
        win.dessin4()
        self.confirm("Interface successfully loaded")
        win2.close()
    def interface5(self):
        win.dessin5()
        self.confirm("Interface successfully loaded")
        win2.close()
    def interface6(self):
        win.dessin6()
        self.confirm("Interface successfully loaded")
        win2.close()
    def interface7(self):
        win.dessin7()
        self.confirm("Interface successfully loaded")
        win2.close()
if __name__ == "__main__":
   app = QApplication([])
   win = Test()
   win2=ButtonsPanel()
   win.show()
   app.exec_()
