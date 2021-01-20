from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem
from classes.drag_button_class import DragButton
from classes.drag_label_class import DragLabel
import classes.database as DB

class TablesButtons(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\floor_designer.ui',self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Floor Designer')
        self.buttons=[]
        self.add_floor.clicked.connect(lambda : self.switch_view(0))
        self.add_tables.clicked.connect(lambda : self.switch_view(1))
        self.floor_box.currentIndexChanged.connect(self.load_table_box)

    def render_floor_designer(self,settings):
        settings.close()
        self.load_boxes()
        #self.setGeometry(300,10,self.width(),self.height())
        self.show()


    def switch_view(self,num):
        self.stackedWidget.setCurrentIndex(num)
    
    def load_boxes(self):
        self.floor_box.clear()
        self.floors_box.clear()
        floors = DB.get_floors()
        
        floor_list = [item['name'] for item in floors]
        for item in sorted(floor_list):
            self.floors_box.addItem(item)
            self.floor_box.addItem(item)
            self.load_table_box()
        
    def load_table_box(self):
        self.table_box.clear()
        tables = DB.get_tables(self.floor_box.currentText())

        table_list = [item['name'] for item in tables]
        for item in sorted(table_list):
            self.table_box.addItem(item)

# ---------------------- STARTS OF FLOORS BUTTONS --------------- #
    def place_floor_buttons(self, view):

        new_button = DragButton(self.floor_name.text())
        new_button.setFixedSize(290,70)
        new_button.setParent(view)
        new_button.show()

        self.buttons.append(new_button)
    
    def save_floor_buttons(self,view):
        for item in self.buttons:
            button = {
                'name':item.text().title(),
                'style':item.styleSheet(),
                'width':item.width(),
                'height':item.height(),
                'x':item.x(),
                'y':item.y()
            }
            DB.save_floor(button)
        for item in self.buttons:
            item.hide()
        self.buttons.clear()
        self.load_boxes()
        view.close()
        view.render_tables_view(view.user)


    def delete_floor(self,view):
        msg = QMessageBox(QMessageBox.Question, 'Warning!', 'Deleting this floor you are deleting all the tables connected to it.\nAre you sure to continue?',QMessageBox.Yes | QMessageBox.No)
        msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        answer= msg.exec()
        if answer == QMessageBox.Yes:
            DB.delete_floor(self.floors_box.currentText())
            self.load_boxes()
            view.close()
            view.render_tables_view(view.user)

#---------------------------------- END OF FLOORS BUTTONS ------------------------#

#--------------------------------- STARTS OF TABLES BUTTONS --------------------- #

    def place_table_buttons(self, view):

        if self.square_selection.isChecked():
            new_button = DragButton(self.table_num.text())
            new_button.setGeometry(self.square_tbl.geometry())
            new_button.setStyleSheet(self.square_tbl.styleSheet())
            new_button.setParent(view)
            new_button.show()

            self.buttons.append(new_button)
        
        elif self.round_selection.isChecked():

            new_button = DragButton(self.table_num.text())
            new_button.setGeometry(self.round_table.geometry())
            new_button.setStyleSheet(self.round_table.styleSheet())
            new_button.setParent(view)
            new_button.show()

            self.buttons.append(new_button)
        else:
            self.box = QMessageBox(QMessageBox.Warning, '','Select a shape please' , QMessageBox.Ok)
            self.box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.box.exec()

    def save_table_button(self, view):
        for button in self.buttons:
            table = {
                'name':button.text().title(),
                'floor': self.floor_box.currentText(),
                'style': button.styleSheet(),
                'width': button.width(),
                'height': button.height(),
                'x': button.x(),
                'y': button.y()
            }
            DB.save_tables(table)
            self.table_num.setText('')
            for item in self.buttons:
                item.hide()
        self.buttons.clear()
        self.load_boxes()
        view.close()
        view.render_tables_view(view.user)

    def delete_table(self,view):
        msg = QMessageBox(QMessageBox.Question, 'Warning!', 'Delete table permanently?',QMessageBox.Yes | QMessageBox.No)
        msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        answer= msg.exec()
        if answer == QMessageBox.Yes:
            DB.delete_table(self.floor_box.currentText(), self.table_box.currentText())
            self.load_table_box()
            view.close()
            view.render_tables_view(view.user)
            view.load_tables(self.floor_box.currentText())

#-------------------------------- END OF TABLES BUTTONS ---------------------------------#

    def cancel(self,view):
        self.close()
        view.close()
        view.render_tables_view(view.user)