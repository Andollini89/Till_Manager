from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox
from classes.tables_view import Table_view
from classes.settings import Settings
from classes.plu import Plu
from classes.users import Users
from classes.buttons import Buttons
from classes.menu_designer import MenuButtons
from classes.floor_designer import TablesButtons
from classes.closed_tabs import Closed
import datetime
import classes.database as DB


class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\login.ui',self)

        self.box = QMessageBox()
        self.setWindowTitle('Login')
        #self.user_data = {}
        self.num_btn_1.clicked.connect(lambda :self.num_btn(1) )
        self.num_btn_2.clicked.connect(lambda :self.num_btn(2) )
        self.num_btn_3.clicked.connect(lambda :self.num_btn(3) )
        self.num_btn_4.clicked.connect(lambda :self.num_btn(4) )
        self.num_btn_5.clicked.connect(lambda :self.num_btn(5) )
        self.num_btn_6.clicked.connect(lambda :self.num_btn(6) )
        self.num_btn_7.clicked.connect(lambda :self.num_btn(7) )
        self.num_btn_8.clicked.connect(lambda :self.num_btn(8) )
        self.num_btn_9.clicked.connect(lambda :self.num_btn(9) )
        self.num_btn_0.clicked.connect(lambda :self.num_btn(0) )
        self.clear_btn.clicked.connect(self.clear_btn_press)
        
        

    def num_btn(self, num):
            number = str(num)
            entry = self.login_entry.text().replace('*','')
            number = entry+number
            #login_entry.delete(0,END)
            self.login_entry.setText(number)

    def clear_btn_press(self):

        self.login_entry.setText('')

    def enter_btn_press(self,tables):
        user_id = self.login_entry.text()
        self.user_data = DB.get_user_data(user_id)
        
        if self.user_data == 1:
            self.show_error_box()
            self.login_entry.setText('')
        else:
            self.login_entry.setText('***')
            
            tables.render_tables_view(self.user_data)
            self.close()

            

    def show_error_box(self):
        
        self.box.setIcon(QMessageBox.Warning)
        self.box.setText('\n  User not found!     \n')
        self.box.setFont(QtGui.QFont("Arial",12))
        self.box.exec()

    def render_login(self, table):
        self.showMaximized()
        table.close()



def render(login,tables,settings,plu,users,buttons,menu_btns,floor,closed):

    # render login page
    login.render_login(tables)
    # render table view page
    login.enter_btn.clicked.connect(lambda:login.enter_btn_press(tables))

    # go back to log in
    tables.logout_btn.clicked.connect(lambda:login.render_login(tables))
    # render settings page
    tables.settings_btn.clicked.connect(lambda:settings.render_settings())
    tables.send_btn.clicked.connect(lambda : tables.send(login))

    # render settings pages on button click
    settings.items_btn.clicked.connect(lambda:plu.render_plu())
    settings.add_users_btn.clicked.connect(lambda:users.render_users())
    settings.add_buttons.clicked.connect(lambda : buttons.render_buttons(settings,tables))
    settings.menu_designer.clicked.connect(lambda : menu_btns.render_menu_buttons(settings))
    settings.floor_design.clicked.connect(lambda: floor.render_floor_designer(settings))

    # place menu button
    menu_btns.place.clicked.connect(lambda : menu_btns.place_btn(tables.menu_layout,menu_btns.name,menu_btns.bg_color,menu_btns.text_color))
    menu_btns.place_2.clicked.connect(lambda : menu_btns.place_btn(tables.sub_layout,menu_btns.sub_name,menu_btns.bg_color_2,menu_btns.text_color_2))
    # close menu btn page and update table view
    menu_btns.cancel.clicked.connect(lambda: menu_btns.cancel_press(tables,login.user_data))
    menu_btns.cancel_2.clicked.connect(lambda: menu_btns.cancel_press(tables,login.user_data))
    # save button created and update table view
    menu_btns.save.clicked.connect(lambda:menu_btns.save_main_button(tables,login.user_data))
    menu_btns.save_2.clicked.connect(lambda:menu_btns.save_sub_button(tables,login.user_data))
    #delete button
    menu_btns.delete_btn.clicked.connect(lambda : menu_btns.delete_button(tables, login.user_data,'main',menu_btns.main_list_box.currentText()))
    menu_btns.delete_btn_2.clicked.connect(lambda : menu_btns.delete_button(tables, login.user_data,'sub',menu_btns.sub_menu_box.currentText(),menu_btns.main_menu_box.currentIndex()))

    menu_btns.main_list_box.currentIndexChanged.connect(lambda : tables.switch_menu(menu_btns.main_list_box.currentIndex()))
    menu_btns.main_menu_box.currentIndexChanged.connect(lambda: menu_btns.fill_sub_menu(tables))

    buttons.cancel_btn.clicked.connect(lambda:buttons.cancel(tables,login.user_data))
    buttons.place_btn.clicked.connect(lambda : buttons.place_btn_func(tables.groupBox))
    buttons.save_btn.clicked.connect(lambda: buttons.save_buttons(tables,login.user_data))

    floor.place.clicked.connect(lambda : floor.place_floor_buttons(tables.floor_plan_menu))
    floor.save_floor.clicked.connect(lambda : floor.save_floor_buttons(tables))
    floor.cancel_floor.clicked.connect(lambda : floor.cancel(tables))
    floor.del_floor.clicked.connect(lambda : floor.delete_floor(tables))
    floor.place_table.clicked.connect(lambda : floor.place_table_buttons(tables.table_frame))
    floor.save_tables.clicked.connect(lambda : floor.save_table_button(tables))
    floor.cancel_table.clicked.connect(lambda: floor.cancel(tables))
    floor.delete_tab.clicked.connect(lambda : floor.delete_table(tables))

    tables.closed_tab.clicked.connect(lambda : closed.render_closed_tabs())
    

    
    
app = QApplication([])
login = Login()
tables = Table_view()
settings = Settings()
users = Users()
plu=Plu()
buttons=Buttons()
menu_btns = MenuButtons()
floor = TablesButtons()
closed = Closed()

DB.init_database()
DB.init_buttons_database()
DB.inint_tables_database()
DB.inint_bills_database()

render(login,tables,settings,plu,users,buttons,menu_btns,floor,closed)
app.exec()

