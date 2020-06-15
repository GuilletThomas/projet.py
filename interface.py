from PySide2.QtWidgets import *

class IHMBateau(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Interface Bateau")
        self.layout = QGridLayout()
        self.setMinimumSize(900,500)

        self.button1 = QPushButton("Load 3D Model")
        self.button2 = QPushButton("Load Image")
        self.button3 = QPushButton("Compute")

        self.label1 = QTextEdit("modele 3D")
        self.label2 = QTextEdit("calculs")


        self.layout.addWidget(self.button1, 1,1,1,2)
        self.layout.addWidget(self.button2, 1,3,1,2)
        self.layout.addWidget(self.button3, 1,5,1,2)

        self.layout.addWidget(self.label1, 2,1,2,4)
        self.layout.addWidget(self.label2, 2,5,2,2)



        self.setLayout(self.layout)

if __name__ == "__main__":
   app = QApplication([])
   ihm = IHMBateau()
   ihm.show()
   app.exec_()

