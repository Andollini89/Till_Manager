from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem



class Settings(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\settings.ui',self)
        self.setWindowTitle('Settings')



    def render_settings(self):
        self.show()