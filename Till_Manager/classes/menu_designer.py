from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem
from classes.drag_button_class import DragButton
import classes.database as DB

class MenuButtons(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\menu_designer.ui',self)
        self.setWindowTitle('Menu Designer')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.buttons_list=[]
        self.colors = ['','white','blue','red', 'brown', 'green', 'purple']
        self.text_color_list = ['','white','red', 'yellow', 'black']
        self.main_menu_btn.clicked.connect(lambda : self.switch_view(0))
        self.sub_menu_btn.clicked.connect(lambda : self.switch_view(1))
        
        

    def render_menu_buttons(self,settings):
        self.settings = settings
        self.fill_comboboxes()
        self.buttons_list=[]
        self.settings.hide()
        self.show()

    def place_btn(self,menu_bar,name,bg,fg):
               
        self.new_button = DragButton(text=name.text())
        self.new_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.new_button.setStyleSheet(f'background-color:{bg.currentText()};color:{fg.currentText()}; border-radius:10; font-size:12pt')
        menu_bar.addWidget(self.new_button) 
        print(self.new_button.styleSheet(),self.new_button.geometry())
        self.buttons_list.append(self.new_button)
        name.setText('')

    def fill_comboboxes(self):
        main_list = DB.get_top_buttons()
        self.main_menu_box.clear()
        self.main_list_box.clear()
        self.bg_color.clear()
        self.bg_color_2.clear()
        self.text_color.clear()
        self.text_color_2.clear()
        for item in main_list:
            self.main_menu_box.addItem(item['name'])
            self.main_list_box.addItem(item['name'])
        for item in self.colors:
            self.bg_color.addItem(item)
            self.bg_color_2.addItem(item)

        for item in self.text_color_list:
            self.text_color.addItem(item)
            self.text_color_2.addItem(item)


    def fill_sub_menu(self,table_view):
        table_view.switch_menu(self.main_menu_box.currentIndex())
        self.sub_menu_box.clear()
        sub_list = DB.get_sub_buttons(self.main_menu_box.currentIndex())
        for item in sub_list:
            self.sub_menu_box.addItem(item['name'])


    def save_main_button(self,view,user):
        for item in self.buttons_list:
            button = {
                'name': item.text().title(),
                'style':item.styleSheet(),
                'width':item.width(),
                'height':item.height(),
                'x':item.x(),
                'y':item.y()
            }
            DB.save_menu_button(button)
        self.buttons_list.clear()
        self.fill_comboboxes()
        view.close()
        view.render_tables_view(user)
    
    def save_sub_button(self,view,user):
        for item in self.buttons_list:
            button = {
                'name': item.text().title(),
                'style':item.styleSheet(),
                'main': self.main_menu_box.currentIndex(),
                'width':item.width(),
                'height':item.height(),
                'x':item.x(),
                'y':item.y()
            }
            DB.save_sub_button(button)
        self.buttons_list.clear()
        self.fill_comboboxes()
        view.close()
        view.render_tables_view(user)

    def delete_button(self,view,user,table,name,main=None):
        DB.delete_button(table,name,main)
        self.fill_comboboxes()
        view.close()
        view.render_tables_view(user)
    
    def switch_view(self,num):
        self.switch_menu.setCurrentIndex(num)

    def cancel_press(self,view,user):
        view.close()
        view.render_tables_view(user)
        self.close()
        self.settings.show()
