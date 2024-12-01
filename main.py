import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.conn = sqlite3.connect('coffee.sqlite')
        self.load_table()

        self.add_btn.clicked.connect(self.add_coffee_form)
        self.upd_btn.clicked.connect(self.edit_coffee_form)

    def load_table(self):
        self.table.clear()
        result = self.conn.cursor().execute('''SELECT * FROM coffee''').fetchall()

        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена $',
             'объем упаковки'])
        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()

    def add_coffee_form(self):
        self.add_addcoffee_form = EditCoffeeForm(self)
        self.add_addcoffee_form.show()

    def edit_coffee_form(self):
        ids = self.selected_ids(self.table)
        if len(ids) == 1:
            self.add_editcoffee_form = EditCoffeeForm(self, ids[0])
            self.add_editcoffee_form.show()
            return
        self.statusBar().showMessage('Выберите 1 кофе')

    def selected_ids(self, table):
        rows = list(set([i.row() for i in table.selectedItems()]))
        ids = [table.item(i, 0).text() for i in rows]
        return ids


class EditCoffeeForm(QMainWindow):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.conn = sqlite3.connect('coffee.sqlite')
        self.coffee_id = coffee_id

        if coffee_id:
            self.save_btn.clicked.connect(self.edit_coffee)
            result = self.conn.cursor().execute('''SELECT * FROM coffee WHERE id = ?''', (coffee_id,)).fetchone()

            self.name.setText(result[1])
            self.pow.setText(result[2])
            self.gr_wh.setText(result[3])
            self.descript.setText(result[4])
            self.price.setText(result[5])
            self.volume.setText(result[6])
        else:
            self.save_btn.clicked.connect(self.add_coffee)

    def add_coffee(self):
        self.get_values()
        if self.get_verdict():
            self.conn.cursor().execute('''INSERT INTO coffee(name, roast_level, ground_whole_beans, taste_description, price, package_volume) 
            VALUES (?, ?, ?, ?, ?, ?)''', (
                self.name_, self.pow_, self.gr_wh_, self.descript_, int(self.price_), self.volume_))
            self.conn.commit()
            self.parent().load_table()
            self.close()
            return
        self.statusBar().showMessage('Неверно заполнена форма')

    def edit_coffee(self):
        self.get_values()
        if self.get_verdict():
            self.conn.cursor().execute(
                '''UPDATE coffee SET name = ?, roast_level = ?, ground_whole_beans = ?, taste_description = ?, price = ?, package_volume = ?
                WHERE id = ?''',
                (self.name_, self.pow_, self.gr_wh_, self.descript_, int(self.price_), self.volume_, self.coffee_id))
            self.conn.commit()
            self.parent().load_table()
            self.close()
            return
        self.statusBar().showMessage('Неверно заполнена форма')

    def get_verdict(self):
        self.get_values()
        if self.name_ and self.pow_ and self.gr_wh_ and self.descript_ and self.volume_ and self.price_:
            return True
        return False

    def get_values(self):
        self.name_ = self.name.text()
        self.pow_ = self.pow.text()
        self.gr_wh_ = self.gr_wh.text()
        self.descript_ = self.descript.text()
        self.price_ = self.price.text()
        self.volume_ = self.volume.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())
