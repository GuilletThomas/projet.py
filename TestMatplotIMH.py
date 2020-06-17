from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy
import matplotlib.pyplot as plt

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Matplotlib Embeding In PyQt5"
        top = 400
        left = 400
        width = 900
        height = 500

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.MyUI()


    def MyUI(self):

        canvas = Canvas(self, width=8, height=4)
        canvas.move(0,0)

        button = QPushButton("Click Me", self)
        button.move(100, 450)

        button2 = QPushButton("Click Me Two", self)
        button2.move(250, 450)


class Canvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 5, dpi = 100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.plot()


    def plot(self):
        listevalMilieu=[11530.629385640828, -3674.3706143591717, 3431.6293856408283, -267.37061435917167]
        axs=plt.axes()
        #axs.axis([min(listeiteration)-0.2*min(listeiteration),max(listeiteration)+0.2*max(listeiteration),min(listePhi)-0.2*min(listePhi),max(listePhi)+0.2*max(listePhi)])
        plt.scatter(numpy.arange(len(listevalMilieu)),listevalMilieu, color = 'blue')
        plt.grid()
        plt.plot(numpy.arange(len(listevalMilieu)),listevalMilieu)

        plt.title('Graph')
        plt.xlabel('Itération')
        plt.ylabel('Résultante des forces N')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
