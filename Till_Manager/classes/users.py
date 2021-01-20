from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem
import classes.database as DB


class Users(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\users.ui',self)
        self.setWindowTitle('Users')
        self.privilege=''

        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.modify_btn.clicked.connect(self.populate_fields)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.search_field.textChanged.connect(self.update_list)
        self.delete_btn.clicked.connect(self.delete_item)


    def render_users(self):
        ''' This function is called when 'add user' is prssed from 'Settings',
            fills the list of user,  and clear text-edits fields'''
        self.clear_fields()
        self.fill_users_list()
        self.show()

    def clear_fields(self):
        ''' the function make the text-edits fields empty'''
        self.name_field.setText(None)
        self.passcode_field.setText(None)

    def radio_btn_checked(self):
        ''' this function check which of the radio btn is checked and return the correct value(STR)'''
        if self.admin_btn.isChecked():
            self.privilege = 'admin'
        elif self.user_btn.isChecked():
            self.privilege = 'user'
        return self.privilege

    def save(self):
        ''' Th save function save the data for a new user or update a esixting user, 
            checking if the fields are compiled with the right type of data,
            oderwise raise an error message box,
            if all goes right, clear fields and update the user list'''
        if self.name_field.text().lower() != '' and (self.passcode_field.text().isdigit() or self.passcode_field.text() !=''):
            new_user={
                'name':self.name_field.text().lower(),
                'passcode':self.passcode_field.text(),
                'user_type':self.radio_btn_checked()
            }
            DB.update_users(new_user)
            self.clear_fields()
            self.box = QMessageBox(QMessageBox.Question, 'Save Successed', '\tUser Saved\t\t', QMessageBox.Ok)
            self.box.exec()
            self.fill_users_list()

        else:
            self.box = QMessageBox(QMessageBox.Warning, 'Error Saving', 'User cannot be saved\t\nRevew insertions and retry\t', QMessageBox.Ok)
            self.box.exec()

    def fill_users_list(self):
        ''' this function fills the list widget with the data taken form the database'''
        self.users_list.clear()
        self.user_list = DB.show_users_list()
        for item in sorted(self.user_list):
            self.users_list.addItem(item.title())

    def populate_fields(self):
        ''' This function take a selected item from the list and 
            when called fills the field with the user data requested from the user '''
        for user in self.users_list.selectedItems():

            user_clicked = DB.populate_users_field(user.text().lower())
            self.name_field.setText(user_clicked['name'].title())
            self.passcode_field.setText(user_clicked['passcode'])
            if user_clicked['user_type']== 'admin':
                self.admin_btn.setChecked(True)
            else:
                self.user_btn.setChecked(True)

    def update_list(self):
        '''The update function perfom a match search,
            showing on the list only the matched users'''
        self.users_list.clear()
        for user in self.user_list :
            if self.search_field.text().lower() in user or self.search_field.text().upper() in user:
                self.users_list.addItem(user)
    
    def delete_item(self):
        ''' the Delete function delete user from the datatbase only after confirmed by the user'''
        self.box = QMessageBox(QMessageBox.Question, 'Warning!', 'The item selected will be deleted permanently!\t\nDo you want to continue?\t',QMessageBox.Yes | QMessageBox.No)
        answer=self.box.exec()
        if answer == QMessageBox.Yes:
            for item in self.users_list.selectedItems():
                if item.text().lower() == 'master':
                    self.box = QMessageBox(QMessageBox.Critical,'Error', 'Master User deletion is denied!')
                    self.box.exec()
                else:
                    DB.delete_user(item.text().lower())
                    self.fill_users_list()

    def cancel(self):
        ''' The cancel function is triggered by the cancel btn and close the page'''
        self.close()