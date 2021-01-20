from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem
import classes.database as DB
from time import sleep



class Plu(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\plu.ui',self)
        self.setWindowTitle('Items PLU')
        #initializate a empti categori list
        self.categories = []
        #connect  buttons to functions
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.cancel)
        self.search_field.textChanged.connect(self.update_item_list)
        self.list_items.doubleClicked.connect(self.populate_fields)
        self.clear_btn.clicked.connect(self.empty_entries_fields)
        self.delete_btn.clicked.connect(self.delete_item)
        self.category_box.currentIndexChanged.connect(self.fill_sub_categories)
        

    def render_plu(self):
        """ Render plu page when 'Item' button in 'Setting' is pressed,
            Full fill items list,
            empty the fields,
            get category list ready """

        self.categories = DB.get_top_buttons()
        self.fill_items_list()
        self.empty_entries_fields()
        self.show()

    def empty_entries_fields(self):
        """ This function will make all text-edit fields empty"""
        self.name_field.setText('')
        self.price_field.setText('')
        self.cost_field.setText('')
        self.vat_field.setText('')
        self.count_field.setText('')
    
    
    def save(self):
        """ The save Function Tries to add Item to the database relatet to the text-edit fields,
            if any of the fiel is empty or not with the right tipe value raise an error message box,
            else, empties the fields, update the list field, and make the user aware that the save is succes"""
        try:
            new_item = {
                'name': self.name_field.text().title(),
                'category': self.category_box.currentText(),
                'sub': self.sub_box.currentText(),
                'price': float(self.price_field.text()),
                'cost': float(self.cost_field.text()),
                'vat': float(str(self.vat_field.text()).replace('%','')), 
                'count':int(self.count_field.text()) 
            }
            DB.insert_into_plu(new_item)
            self.empty_entries_fields()
            self.box = QMessageBox(QMessageBox.Question, 'Save Successed', '\tItem Saved\t\t', QMessageBox.Ok)
            self.box.exec()
            self.fill_items_list()
        except (KeyError, TypeError, ValueError):
            self.box = QMessageBox(QMessageBox.Warning, 'Error Saving', 'The item cannot be saved\t\nRevew insertions and retry\t', QMessageBox.Ok)
            self.box.exec()

    def fill_items_list(self):
        ''' Any time this function is called fills the list of items by getting the data stored in the database,
            sorting them in ascendet order, and populate the category box with the mains categories  '''
        self.list_items.clear()
        self.category_box.clear()
        self.item_list = DB.show_item_list()
        for item in sorted(self.item_list):
            self.list_items.addItem(item)
        for item in self.categories:
            self.category_box.addItem(item['name'])

    def fill_sub_categories(self):
        self.sub_box.clear()
        self.sub_categories=DB.get_sub_buttons(self.category_box.currentIndex())
        for item in self.sub_categories:
            self.sub_box.addItem(item['name'].title())
   
    def update_item_list(self):
        ''' This function is called any time the search field is modified,
            to perform a match based search for the user,
            it clear the list widget and repopulate it only with the items matching '''
        self.list_items.clear()
        for item in self.item_list:
            if self.search_field.text().lower() in item or self.search_field.text().upper() in item:
                self.list_items.addItem(item)


    def populate_fields(self):
        ''' The function is called when the user doubleclick on a item in the list and
            fills the text-edits fields with the data correlated from database
                TODO: MAKE THE CATEGORY AND SUB CATEGORY RIGHT'''
        for item in self.list_items.selectedItems():
            clicked_item = DB.populate_plu_fields(item.text())

            self.name_field.setText(clicked_item['name'].title())
            self.category_box.setCurrentText(clicked_item['category'])
            self.sub_box.setCurrentText(clicked_item['sub'])
            self.price_field.setText(f"{clicked_item['price']:.2f}")
            self.cost_field.setText(f"{clicked_item['cost']:.2f}")
            self.vat_field.setText(f"{clicked_item['vat']:.1f}%")
            self.count_field.setText(str(clicked_item['count']))
        
    def delete_item(self):
        ''' The delete function delete from the database a selected item,
            confirming with the user if has tobe performed'''
        self.box = QMessageBox(QMessageBox.Question, 'Warning!', 'The item selected will be deleted permanently!\t\nDo you want to continue?\t',QMessageBox.Yes | QMessageBox.No)
        answer=self.box.exec()
        if answer == QMessageBox.Yes:
            for item in self.list_items.selectedItems():
                DB.delete_item(item.text())
                self.fill_items_list()
            
    def cancel(self):
        ''' When the cancel function is called close the plu page'''
        self.close()