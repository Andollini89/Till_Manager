from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem
import classes.database as DB


class Closed(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\closed_tabs.ui',self)
        self.setWindowTitle('Closed Tabs')
        header = self.closed_tables.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.closed_tables.setColumnCount(4)


    def render_closed_tabs(self):
        self.show()
        self.populate_table()

    def populate_table(self):
        self.closed_tables.setRowCount(0)
        list_of_tabs = DB.get_closed()
        print(list_of_tabs)
        for item in list_of_tabs:
            row_count = self.closed_tables.rowCount()
            
            self.closed_tables.insertRow(row_count)
            self.closed_tables.setItem(row_count,0, self.create_table_item(item['tab']))
            self.closed_tables.setItem(row_count,1, self.create_table_item(item['user']))
            self.closed_tables.setItem(row_count,2, self.create_table_item('£'+ item['tot']))
            self.closed_tables.setItem(row_count,3, self.create_table_item(item['time']))

    def create_table_item(self, text):
        ''' this function create a generic item to use to populate the order table'''
        item = QTableWidgetItem()
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item
