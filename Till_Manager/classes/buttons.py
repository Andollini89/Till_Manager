from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem
from classes.drag_button_class import DragButton
import classes.database as DB


class Buttons(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\buttons.ui',self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Buttons')
        self.colors = ['','white','blue','red', 'brown', 'green', 'purple']
        self.text_color_list = ['','white','red', 'yellow', 'black']
        self.buttons=[]
        
        self.main_menu.currentIndexChanged.connect(self.fill_sub_menu)
        self.sub_cat_box.currentIndexChanged.connect(self.fill_items_menu)
        self.bg_color.currentIndexChanged.connect(self.set_button_colors)
        self.text_color.currentIndexChanged.connect(self.set_button_colors)

    def render_buttons(self, settings, tables):
        self.view = tables
        self.settings = settings
        self.category = DB.get_top_buttons()
        self.settings.hide()
        self.show()
        self.fill_main_menu()
    

    def fill_main_menu(self):
        self.main_menu.clear()
        for item in self.category:
            self.main_menu.addItem(item['name'].title())
        for item in sorted(self.colors):
            self.bg_color.addItem(item.title())
        for item in sorted(self.text_color_list):
            self.text_color.addItem(item.title())


    def fill_sub_menu(self):
        self.sub_cat_box.clear()
        self.sub_category = DB.get_sub_buttons(self.main_menu.currentIndex())
        for item in self.sub_category:
            self.sub_cat_box.addItem(item['name'])
        self.view.switch_menu(self.main_menu.currentIndex())
    
    def fill_items_menu(self):
        self.item_box.clear()
        self.items = DB.get_items_by_sub_cat(self.sub_cat_box.currentText())
        for item in sorted(self.items):
            self.item_box.addItem(item)
        self.view.switch_items_menu(self.main_menu.currentIndex(), self.sub_cat_box.currentIndex())
    
    def set_button_colors(self):
        self.btn_rectangular.setStyleSheet(f'background-color:{self.bg_color.currentText()}; color:{self.text_color.currentText()}; border-radius:10; font-size:12pt')
        self.btn_square.setStyleSheet(f'background-color:{self.bg_color.currentText()}; color:{self.text_color.currentText()}; border-radius:10; font-size:12pt')
    
    def place_btn_func(self, view):

        if self.check_btn_1.isChecked():
            new_button = DragButton(self.btn_rectangular.icon(),self.item_box.currentText())
            new_button.setGeometry(self.btn_rectangular.geometry())
            new_button.setStyleSheet(self.btn_rectangular.styleSheet())
            new_button.setParent(view)
            
            new_button.show()
            self.buttons.append(new_button)

        elif self.check_btn_2.isChecked():
            new_button = DragButton(self.btn_square.icon(),self.item_box.currentText())
            new_button.setGeometry(self.btn_square.geometry())
            new_button.setStyleSheet(self.btn_square.styleSheet())
            new_button.setParent(view)
            
            new_button.show()
            self.buttons.append(new_button)
            
        else:
            self.box = QMessageBox(QMessageBox.Warning, '','Select a button shape please' , QMessageBox.Ok)
            self.box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.box.exec()
            
    def save_buttons(self,view,user):
        for item in self.buttons:
            button = {
                'name': item.text().title(),
                'main': self.main_menu.currentIndex(),
                'sub': self.sub_cat_box.currentIndex(),
                'style':item.styleSheet(),
                'width':item.width(),
                'height': item.height(),
                'x': item.x(),
                'y': item.y()
            }
            item.hide()
            DB.save_item_buttons(button)
        self.buttons.clear()
        view.close()
        view.render_tables_view(user)

    def delete_button(self,view,user,table,name,main=None):
        DB.delete_button(table,name,main)
        view.close()
        view.render_tables_view(user)

    def cancel(self,view,user):
        self.close()
        view.close()
        view.render_tables_view(user)
        self.settings.show()