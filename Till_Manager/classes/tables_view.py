from PyQt5 import QtWidgets, QtGui, uic,QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QMessageBox, QTableWidgetItem, QAbstractItemView
import os
import tempfile
import win32api
import win32print
import datetime
import classes.database as DB



class Table_view(QWidget):
    def __init__(self):
        super().__init__()
        #self.login = Login()
        uic.loadUi('ui\\table_view2.ui',self)
        self.setWindowTitle('My Till Manager')
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.items = []

        # Buttons connected to swtich frame
        self.tables_btn.clicked.connect(lambda : self.switch_floor_frame())

     # Set Hearder size in order to have enough space
        header = self.orders_table.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.orders_table.setColumnCount(3)

        Vheader = self.totals.verticalHeader()
        Vheader.setFixedSize(300,110)
        
        # connect action buttons to 'orders_table'
        self.snacks_btn.clicked.connect(lambda : self.action_into_table(self.snacks_btn.text()))
        self.starters_btn.clicked.connect(lambda : self.action_into_table(self.starters_btn.text()))
        self.mains_btn.clicked.connect(lambda : self.action_into_table(self.mains_btn.text()))
        self.desserts_btn.clicked.connect(lambda : self.action_into_table(self.desserts_btn.text()))
        self.drinks_btn.clicked.connect(lambda : self.action_into_table(self.drinks_btn.text()))

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

        self.delete_item_btn.clicked.connect(self.delete_items)
        self.send_stay.clicked.connect(self.send_and_stay)
        self.close_tab.clicked.connect(self.close_tab_save_and_delete)
        self.bill_btn.clicked.connect(self.print_bill)
 
 
 
 
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.current_time)
        self.timer.start(1000)

    def render_tables_view(self, user):
        ''' This function will show the main window after the Login '''
        self.user=user
        if self.user['privilege'] == 'admin':
            self.settings_btn.show()
        else:
            self.settings_btn.hide()
        self.showMaximized()
        self.load_top_buttons(self.menu_layout)
        self.load_floors()
        
        self.user_privilege_label.setText(self.user['privilege'].title())
        self.username_label.setText(self.user['name'].title())


    def load_floors(self):
        selection = DB.get_floors()
        self.buttons=[]
        for item in selection:
            button = QtWidgets.QPushButton(item['name'])
            button.setGeometry(item['x'],item['y'],item['width'],item['height'])
            button.setParent(self.floor_plan_menu)
            button.clicked.connect(lambda checked,name=item['name']: self.load_tables(name))
            self.buttons.append(button)
        for button in self.buttons:
            button.show()

    def load_tables(self,floor_name):
        selection = DB.get_tables(floor_name)
        for button in self.table_frame.findChildren(QtWidgets.QPushButton):
            button.hide()
        self.buttons=[]
        for item in selection:
            button = QtWidgets.QPushButton(item['name'])
            button.setFlat(True)
            button.setGeometry(item['x'],item['y'],item['width'],item['height'])
            button.setStyleSheet(item['style'])
            button.setParent(self.table_frame)
            button.clicked.connect(lambda checked,button=button,text=item['name']: self.open_table(button,text))
            self.buttons.append(button)
        for button in self.buttons:
            button.show()
        

    def load_top_buttons(self,place):
        for i in reversed(range(place.count())): 
            place.itemAt(i).widget().deleteLater()
        self.buttons= []
        selection = DB.get_top_buttons()
        for i in range(len(selection)):
            button = QtWidgets.QPushButton(text=selection[i]['name'],flat=False)
            button.setGeometry(selection[i]['x'],selection[i]['y'],selection[i]['width'],selection[i]['height'])
            button.setStyleSheet(selection[i]['style'])
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            button.clicked.connect(lambda checked,index=i: self.switch_menu(index))
            self.buttons.append(button)

        for button in self.buttons:
            place.addWidget(button)


    def current_time(self):
        ''' This function update the label "time" every second'''
        current_time = str(datetime.datetime.now()).split('.')
        self.time_label.setText(current_time[0])
    
    def switch_menu(self,index):
        ''' This function switch betveen the sub menus when a "menu_btn" is pressed
            and put the main view always on index 1'''
        self.main_view.setCurrentIndex(1)
        for i in reversed(range(self.sub_layout.count())): 
            self.sub_layout.itemAt(i).widget().deleteLater()
        self.buttons= []
        selection = DB.get_sub_buttons( index)
        for i in range(len(selection)):
            button = QtWidgets.QPushButton(text=selection[i]['name'],flat=False)
            button.setGeometry(selection[i]['x'],selection[i]['y'],selection[i]['width'],selection[i]['height'])
            button.setStyleSheet(selection[i]['style'])
            button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

            button.clicked.connect(lambda checked,main= selection[i]['main'],index=i: self.switch_items_menu(main,index))
            self.buttons.append(button)

        for button in self.buttons:
            self.sub_layout.addWidget(button)

        for button in self.groupBox.findChildren(QtWidgets.QPushButton):
            button.hide()
        
        


    def switch_items_menu(self,main,index):
        ''' This function swap the items view on press of sub_menu_btns'''
        for item in self.items:
            item.hide()
        self.items.clear()
        selection = DB.get_item_buttons(main, index)
        for i in range(len(selection)):
            button = QtWidgets.QPushButton(text=selection[i]['name'],flat=False)
            button.setGeometry(selection[i]['x'],selection[i]['y'],selection[i]['width'],selection[i]['height'])
            button.setStyleSheet(selection[i]['style'])
            button.setParent(self.groupBox)
            button.clicked.connect(lambda checked, name=button.text(): self.insert_product(name))
            

            self.items.append(button)

        for button in self.items:
            button.show()

    def switch_floor_frame(self):
        ''' This function set mainview on 0 index and the floor_plan_display on the index requested'''
        self.main_view.setCurrentIndex(0)
        self.tab_numb.setText('')
            
    
    def insert_product(self, item):
        product = DB.get_item(item)
        row_position = self.orders_table.rowCount()
        for row in range(row_position):
            if self.orders_table.item(row,1).text() == product['name']:
                if self.number_entry_field.text():
                    qty = f"{int(self.number_entry_field.text()) + int(self.orders_table.item(row,0).text())}"
                    price = f"{(float(qty)*float(product['price'])):.2f}"
                    self.orders_table.item(row,0).setText(qty)
                    self.orders_table.item(row,2).setText(price)
                    self.update_totals()
                    return
                else:
                    qty = f"{int(self.orders_table.item(row,0).text()) + 1}"
                    price = f"{(float(qty)*float(product['price'])):.2f}"
                    self.orders_table.item(row,0).setText(qty)
                    self.orders_table.item(row,2).setText(price)
                    self.update_totals()
                    return
        if self.number_entry_field.text():
            qty = self.number_entry_field.text()
        else:
            qty = '1'
        name = self.create_table_item(product['name'])
        price = self.create_table_item(f"{(float(qty) * float(product['price'])):.2f}")
        
        self.orders_table.insertRow(row_position)
        self.orders_table.setItem(row_position, 0, self.create_table_item(qty))
        self.orders_table.setItem(row_position, 1, name)
        self.orders_table.setItem(row_position, 2, price)
        self.clear_btn_press()
        self.orders_table.scrollToItem(name, QAbstractItemView.EnsureVisible)
        self.update_totals()
        
    def send_and_stay(self):
        row_position = self.orders_table.rowCount()
        tabs=[]
        for row in range(row_position):
            try:
                tab ={
                    'tab':self.tab_numb.text(),
                    'qty':self.orders_table.item(row,0).text(),
                    'item':self.orders_table.item(row,1).text(),
                    'price':self.orders_table.item(row,2).text(),
                }
            except:
                tab = {
                    'tab':self.tab_numb.text(),
                    'qty':None,
                    'item':self.orders_table.item(row,1).text(),
                    'price':None,
                }
            tabs.append(tab)
        for tab in tabs:
            DB.save_tab(tab)

    def send(self,login):
        self.send_and_stay()
        login.render_login(self)

    def get_tab_items(self,tab):
        
        items = DB.get_tab(tab)
        self.orders_table.setRowCount(0)
        for item in items:
            row_position = self.orders_table.rowCount()
            try:#if int(item['qty']) != 0 or int(item['price']) != 0:
                self.orders_table.insertRow(row_position)
                self.orders_table.setItem(row_position,0,self.create_table_item(item['qty']))
                self.orders_table.setItem(row_position,1,self.create_table_item(item['item']))
                self.orders_table.setItem(row_position,2,self.create_table_item(item['price']))
            except:#else:
                self.orders_table.insertRow(row_position)
                blue_item = self.create_table_item(item['item'])
                blue_item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
                self.orders_table.setItem(row_position,1,blue_item)
        self.update_totals()

    def action_into_table(self, item):
        ''' Insert new row into orders table '''
        item = self.create_table_item(item)
        item.setForeground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.blue)))
        row_position = self.orders_table.rowCount()
        self.orders_table.insertRow(row_position)
        
        self.orders_table.setItem(row_position , 1, item)
        
        self.clear_btn_press()
        self.orders_table.scrollToItem(item, QAbstractItemView.PositionAtTop)
        
    def update_totals(self):
        sub_tot = 0
        for row in range(self.orders_table.rowCount()):
            try:
                sub_tot = sub_tot + float(self.orders_table.item(row,2).text())
            except:
                sub_tot = sub_tot
        service = (sub_tot * 12.5)/ 100
        tot = service + sub_tot
        self.totals.item(0,0).setText(f"{sub_tot:.2f}")
        self.totals.item(1,0).setText(f"{service:.2f}")
        self.totals.item(2,0).setText(f"{tot:.2f}")

    def create_table_item(self, text):
        ''' this function create a generic item to use to populate the order table'''
        item = QTableWidgetItem()
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        return item


    def num_btn(self, num):
        ''' Write numbers into the text field '''
        number = str(num)
        entry = self.number_entry_field.text()
        number = entry+number
        #login_entry.delete(0,END)
        self.number_entry_field.setText(number)

    def clear_btn_press(self):
        ''' Clear the entry text field '''
        self.number_entry_field.setText('')
    
    def delete_items(self):
        ''' the delete function delete items from the order table only if not saved in the database'''
        rows = set()
        items_list=[]
        for index in self.orders_table.selectedIndexes():
            rows.add(index.row())

        for row in sorted(rows, reverse=True):
            items_list.append(self.orders_table.item(row,1).text())
            self.orders_table.removeRow(row)
        print(items_list)
        for item in items_list:
            DB.delete_items_from_tab(self.tab_numb.text(),item)
        
        self.update_totals()
    def open_table(self,button,text):
        self.table_button = button
        self.table_button.setStyleSheet(f"{self.table_button.styleSheet()}; background-color:'yellow'")
        self.tab_numb.setText(text)
        self.main_view.setCurrentIndex(1)
        self.get_tab_items(str(text))

    def close_tab_save_and_delete(self):
        row_count = self.orders_table.rowCount()
        qtys = []
        items = []
        prices = []

        for row in range(row_count):
            try:
                qtys.append(self.orders_table.item(row,0).text())
                items.append(self.orders_table.item(row,1).text())
                prices.append(self.orders_table.item(row,2).text())
            except:
                items.append(self.orders_table.item(row,1).text())
        
        closed_tab = {
            'user':self.username_label.text(),
            'tab': self.tab_numb.text(),
            'qty': qtys,
            'item': items,
            'price': prices,
            'sub': self.totals.item(0,0).text(),
            'service':self.totals.item(1,0).text(),
            'tot':self.totals.item(2,0).text()
        }
        DB.save_closed_tab(closed_tab)
        DB.delete_tab_from_opens(self.tab_numb.text())
        self.table_button.setStyleSheet(f"{self.table_button.styleSheet()}; background-color:'lightblue'")
        self.orders_table.setRowCount(0)

    
    def print_bill(self):
        self.send_and_stay()
        tab = DB.get_tab(self.tab_numb.text())
        file_name =tempfile.mktemp(".txt")
        file = open(file_name, 'w')

        print(self.orders_table.horizontalHeaderItem(0).text()+'\t',end='',file=file)
        print(self.orders_table.horizontalHeaderItem(1).text()+'\t',end='',file=file)
        print(self.orders_table.horizontalHeaderItem(2).text()+'\t',end=2*'\n',file=file)

        for row in tab:
            if len(row['item']) < 7:
                if row['price']:
                    print(row['qty']+'\t'+ row['item']+'\t\t'+('£' + row['price']), file=file)
                else:
                    print('\t'+ row['item'], file=file)
            else:
                if row['price']:
                    print(row['qty']+'\t'+ row['item']+'\t'+('£' + row['price']), file=file)
                else:
                    print('\t'+ row['item'], file=file)

        print(3*'\n'+'\t'+self.totals.verticalHeaderItem(0).text() + '\t' + '£' + self.totals.item(0,0).text(),file=file)
        print('\t'+ self.totals.verticalHeaderItem(1).text() + '\t' + '£'+ self.totals.item(1,0).text(),file=file)
        print('\t'+ self.totals.verticalHeaderItem(2).text() + '\t\t' + '£'+ self.totals.item(2,0).text(),file=file)

        printer = win32print.GetDefaultPrinter()
        win32api.ShellExecute(0,"print",file_name, f"{printer}",".",0)
        file.close()


        
