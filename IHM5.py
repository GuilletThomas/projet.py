from PySide2.QtWidgets import *
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d
from DichotomyOfficiel import *
from mpl_toolkits.mplot3d import axes3d, Axes3D #car erreur "unknown projection '3d'"
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#pour l'utilsation de Axes3D --> source "https://stackoverflow.com/questions/3810865/matplotlib-unknown-projection-3d-error"

class Test(QWidget):
    def __init__(self,fichier=None):
        self.__fichier=fichier
        QWidget.__init__(self)
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"

        #rafraichissement
        self.canvas.draw()

        self.setWindowTitle("Interface Bateau")
        self.layout = QGridLayout()
        self.setMinimumSize(900, 500)

        self.button1 = QPushButton("Load 3D Model")
        self.button2 = QPushButton("Load Graph")
        self.button3 = QPushButton("Compute")
        self.label1=QLabel("Niveau d'eau initial (m)")
        self.label2=QLabel("Précision (m)")
        self.label3=QLabel("Masse (kg)")
        self.label = QTextEdit("calculs")
        self.label11 = QLineEdit()
        self.label22 = QLineEdit()
        self.label33=QLineEdit()
        self.layout.addWidget(self.button1, 1, 1, 1, 2)
        self.layout.addWidget(self.button2, 1, 3, 1, 2)
        self.layout.addWidget(self.button3, 1, 5, 1, 2)

        self.layout.addWidget(self.canvas,3,1,2,4)
        self.layout.addWidget(self.label, 3, 5, 2, 2)
        self.layout.addWidget(self.label1,2,1,1,1)
        self.layout.addWidget(self.label11,2,2,1,1)

        self.layout.addWidget(self.label2,2,3,1,1)
        self.layout.addWidget(self.label22,2,4,1,1)

        self.layout.addWidget(self.label3,2,5,1,1)
        self.layout.addWidget(self.label33,2,6,1,1)

        self.button1.clicked.connect(self.clic)
        self.button3.clicked.connect(self.cliccompute)

        self.setLayout(self.layout)

    def clic(self): #Afficher le Menu du Load Image
        win2.show()
    def cliccompute(self):
        NiveauDeau=float(self.label11.text())
        Precision=float(self.label22.text())
        if NiveauDeau<0 or NiveauDeau>1:  #L'eau doit être comprise entre ces deux niveaux, sinon on demande un nouvel input
            self.label11.setText("Doit être compris entre 0 et 1")
        if Precision<0:
            self.label22.setText("Doit être >0")
        else:
            self.cliccompute2()
    def cliccompute2(self):
        if self.__fichier!=None:
            Precision=float(self.label22.text())
            NiveauDeau=float(self.label11.text())
            if self.label33.text()!='':
                masse=float(self.label33.text())
            else:
                masse=None

            listevalNiveauDeau,listeCalculNiveauDeau=dicho(Precision,self.__fichier,NiveauDeau,masse)
            #mettre precision
            self.label.setText("Niveau d'eau pour atteindre l'équilibre à "+ str(Precision) +" m près "+str(listevalNiveauDeau[-1])+"m. Pour ce niveau d'eau, Pa-P="+str(listeCalculNiveauDeau[1]))

    def dessin(self):
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('V_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='V_HULL_Normals_Outward.STL'
        self.__fichier=fichiername
    def dessin2(self):
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Rectangular_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='Rectangular_HULL_Normals_Outward.STL'
        self.__fichier=fichiername
    def dessin3(self):
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Cylindrical_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
        fichiername='Cylindrical_HULL_Normals_Outward.STL'
        self.__fichier=fichiername


class ButtonsPanel(QWidget):                 #Interface Menu du Load Image, on choisit laquelle
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Choix du Model")
        self.layout = QHBoxLayout()
        self.Button=QPushButton("Premier Objet")
        self.Button2=QPushButton("Deuxieme Objet")
        self.Button3=QPushButton("3e Objet")
        self.layout.addWidget(self.Button)
        self.layout.addWidget(self.Button2)
        self.layout.addWidget(self.Button3)
        self.setLayout(self.layout)
        self.Button.clicked.connect(self.interface1)
        self.Button2.clicked.connect(self.interface2)
        self.Button3.clicked.connect(self.interface3)
    def confirm(self):                                 #Confirmer l'interface chargée
        self.Notif=QMessageBox()
        self.Notif.setWindowTitle("Info") ##########
        self.Notif.setText("Interface chargée avec succès")
        self.Notif.exec_()

    def interface1(self):                        #Si on Load l'interface 1
        win.dessin()
        self.confirm()
        win2.close()
    def interface2(self):
        win.dessin2()
        self.confirm()
        win2.close()

    def interface3(self):
        win.dessin3()
        self.confirm()
        win2.close()

if __name__ == "__main__":
   app = QApplication([])
   win = Test()
   win2=ButtonsPanel()
   win.show()
   app.exec_()
