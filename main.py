import random
import sys

from PyQt6 import uic
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication


class Ex(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)

        self.pushButton.clicked.connect(self.draw)
        self.paint = False

    def draw(self):
        self.paint = True
        self.update()

    def paintEvent(self, a0):
        if self.paint:
            color = QColor(255, 255, 0)
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
