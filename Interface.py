from PySide2.QtWidgets import *
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d

from mpl_toolkits.mplot3d import axes3d, Axes3D #car erreur "unknown projection '3d'"
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#pour l'utilsation de Axes3D --> source "https://stackoverflow.com/questions/3810865/matplotlib-unknown-projection-3d-error"

class Test(QWidget):
    def __init__(self):
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
        self.button2 = QPushButton("Load Image")
        self.button3 = QPushButton("Compute")

        self.label = QTextEdit("calculs")

        self.layout.addWidget(self.button1, 1, 1, 1, 2)
        self.layout.addWidget(self.button2, 1, 3, 1, 2)
        self.layout.addWidget(self.button3, 1, 5, 1, 2)

        self.layout.addWidget(self.canvas,2,1,2,4)
        self.layout.addWidget(self.label, 2, 5, 2, 2)
        self.button1.clicked.connect(self.clic)

        self.setLayout(self.layout)

    def clic(self): #Afficher le Menu du Load Image
        win2.show()

    def dessin(self):
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('V_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
    def dessin2(self):
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Rectangular_HULL_Normals_Outward.stl')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()
    def dessin3(self):
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"
        #dessin 3d
        your_mesh = mesh.Mesh.from_file('Cylindrical_HULL_Normals_Outward.STL')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)
        self.canvas.draw()


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
