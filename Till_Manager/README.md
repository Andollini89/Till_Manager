# My Till Manager

### **_My Till Manager_** is a Python and SQlite based program for Restaurants, Bars and Pubs.
### It has a GUI Interface create with `QT5` to make the use easy and intuitive.
### **_My Till Manager_** provides:
- _Floor designer_;
- _Menu designer_;
- _Item Buttons designer_
### With **_My Till Manager_** it's easy to save tons of products,  users and has easy access to Customers Tabs and Print their bills.
***
## Index
- **[Requisites](#Requisites)**
- **[Usage](#Usage)**
- **[User Guide](#Get-Started)**
  - [Users](#Users)
  - [Floor Designer](#Floor-Designer)
  - [Tables](#Tables)
  - [Main Menus](#Main-Menus)
  - [Items Menus](#Sub-Menus)
  - [Items / PLU](#Items-/-PLU)
  - [Item buttons](#Item-Buttons)
***
## OS:
 - Windows 10.
*** 
## Requisites
### Download [Python 3](https://www.python.org/downloads/release/python-391/) from the official web site.
 - Install Python and check the add Path box.
### Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyqt5 and pywin32.
#### Open Command Prompt and run the following command:
- pip install pyqt5
- pip install pywin32
***
## Usage
- Download from Github the [Till Manager](https://github.com/Andollini89/Till_manager.git).
- From Command Prompt run the command __cd__ to reach the folder Till_Manager.

        (Exemple: cd C:\Users\"User_Name"\Desktop\Till_Manager) 
- Now run the following command:
        
        py Manager.py
***
## Get Started
#### Once you have started the program you will be in the Login Page for the first time use a "0000" code to login.
### **Users**
#### Now is time to __Add a User__ and the passcode: in the right top corner you can find the settings button, click on it and then click on the **_Users_** button and you will be enter in the users page.
#### Now on the right side you can use the blank boxes write,passcode and check admin to allow yourself to use the settings.
### **Floor Designer**
#### Close the **Users** page and let start design your own table settings plan: click on **Floor Designer** and select **_Add Floor_**, use the text box to give a name to the room you are creating and press on the **Place** button at the bottom right. You can now see you button in it's own designed space click and hold the button to move it where you like and click on __Save__ button to save it's position for the fures accesses.
#### You have now created and saved a new room for your tables. 
#### [__Deleting a floor would also delete all the tables connected to it, so be carefull.__](#)
### **Tables**
#### Let's add some tables now! 

#### Click on the __Add Tables__ button, select the floor you want to add table to, give it a number or a name, select the shape and then use the **_Place_** button to make it appear on the screen ( You can place as many tables you like before save ), click and hold the table you've created to move it around the tables section.

#### [**Place them all in the final position before to press the _Save_ button as they can not be moved anymore after saved**.](#) (The feature is in development) 

#### You can also delete a single teble by selecting it from the list and clicking the __Delete__ button.

#### Wow! You have tables now.
### **Main Menus**
#### Whenever you click on a table you are going to open a tab for this table that will be saved in a database of open tables, but first let's create some __Categories Menus__ where connect some __Items Menus__ and some real __Items__ to sell.

#### Starting with the **_Main Category Menus_**: Back on the Setting page  click on the __Menu Designer__ and then on __Main Menu__ at the top letf.

#### Give now a name to your Menu button, select a _Beckground_ color and the _Text color_ from the list ( More colors will be added in the future ) and then click on the __Place__ button. This time the buttons are placed automatically in the top designed space one after another.
#### __Save__ and let's move on to make a detailed __Items Menus__ for each of the __Main Menus__.
### **Sub Menus**
#### Click on the __Sub Menu__ button at the top right of _Menu Designer_, select the __Main Menu__ and then give a name to the __Sub Menu__ choose the colors and place it.
#### [**Remember to choose the _Main Menu_ before place and save otherwise you may find the button in a different place as you may want it!**](#)

#### Now we can insert the actual __Items__.
### **Items / PLU**
(Price Look Up)
#### From __Settings__ click on **_Modify Items_**, you are now ready to insert all the Items from your inventory.
#### Insert in the fields:
- Reference name;
- Select Main Category;
- Select the Sub Category;
- Selling Price;
- Cost Price;
- VAT persentage;
- Quantity of items in stock.
#### __Cost price__, __VAT__ and __Stock Quantity__ have to be implemented for statistics of selling and GP calculation. (Ready soon)
#### **Save** and the list of items on left side of the page will be update.
#### You can also _modify existing item_ by _double clicking_ on the item in the list and the fields will autocomplete for you to modify.
#### For _delete_ an __Item__ select it from the list and press __Delete__.
#### Wow you inserted all you menu in the program! I know is a time consuming task, but all the good things require effort and time!
#### Let's make them usable now.

### **Item Buttons**