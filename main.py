import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Ex(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.conn = sqlite3.connect('coffee.sqlite')
        self.load_table()

    def load_table(self):
        result = self.conn.cursor().execute('''SELECT * FROM coffee''').fetchall()

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена $', 'объем упаковки'])
        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Ex()
    ex.show()
    sys.exit(app.exec())
