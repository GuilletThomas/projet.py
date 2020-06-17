from PySide2.QtWidgets import *
import matplotlib.pyplot as plt
from stl import mesh
from mpl_toolkits import mplot3d

from mpl_toolkits.mplot3d import axes3d, Axes3D #car erreur "unknown projection '3d'"
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#pour l'utilsation de Axes3D --> source "https://stackoverflow.com/questions/3810865/matplotlib-unknown-projection-3d-error"

class Test(QWidget):
    def __init__(self, nomFichier):
        QWidget.__init__(self)
        self.nomFichier = nomFichier
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        ax = Axes3D(self.fig) #erreur "unknown projection '3d'"

        #dessin 3d
        your_mesh = mesh.Mesh.from_file(self.nomFichier)
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
        scale = your_mesh.points.flatten(-1)
        ax.auto_scale_xyz(scale, scale, scale)

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


        self.setLayout(self.layout)

if __name__ == "__main__":
   app = QApplication([])
   ihm = Test('Rectangular_HULL_Normals_Outward.STL')
   ihm.show()
   app.exec_()