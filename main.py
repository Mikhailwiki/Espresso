import random
import sys

from PyQt6 import uic
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication
from UI import Ui_MainWindow


class Ex(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.draw)
        self.paint = False

    def draw(self):
        self.paint = True
        self.update()

    def paintEvent(self, a0):
        if self.paint:
            r, g, b = random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)
            color = QColor(r, g, b)
            radius = random.randint(20, 50)
            qp = QPainter()
            qp.begin(self)
            qp.setBrush(color)
            qp.drawEllipse(QPointF(50, 50), float(radius), float(radius))
            qp.drawEllipse(QPointF(200, 50), float(radius), float(radius))
            qp.end()
            self.paint = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ex()
    ex.show()
    sys.exit(app.exec())
