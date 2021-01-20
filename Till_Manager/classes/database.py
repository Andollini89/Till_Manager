from cs50 import SQL




# ======================== starting of Item and users database =====================#
def init_database():
    
    # Create a database if not exist
    open("till_manager.db","a").close()
    # Open database
    db = SQL("sqlite:///till_manager.db")
    
    # Create a User TABLE
    db.execute(""" CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        passcode TEXT NOT NULL,
        user_privilege TEXT NOT NULL)""")
    
    db.execute(""" CREATE TABLE IF NOT EXISTS plu (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        category TEXT NOT NULL,
        sub_category TEXT NOT NULL,
        price NUMERIC NOT NULL,
        cost_price NUMERIC, 
        vat NUMERIC,
        stock_count INTEGER NOT NULL)
        """)    
    
    # Create Master user for the first time running
    superuser = db.execute("SELECT * FROM users WHERE name='master'")
    
    if not superuser:
        db.execute("INSERT INTO users (name, passcode, user_privilege) VALUES(:name, :passcode, :user_type)",
            name= 'master',
            passcode= '0000',
            user_type= 'admin'
        )
def update_users(user):

    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT passcode, name FROM users")

    codes = [code['passcode'] for code in rows]
    names = [name['name'].lower() for name in rows]

    if user['passcode'] not in codes:
        if user['name'].lower() not in names:
            db.execute("INSERT INTO users (name, passcode, user_privilege) VALUES(:name, :passcode, :user_type)",
                name= user['name'].lower(),
                passcode= user['passcode'],
                user_type= user['user_type']
                )
        else: 
            db.execute("UPDATE users SET name=:name, passcode=:passcode, user_privilege=:user_type WHERE name=:name",
                name=user['name'].lower(),
                passcode= user['passcode'],
                user_type= user['user_type']
                )


def get_user_data(passcode):
    ''' Define a function tha query db for passcode and get back user and users privilege '''

    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT name, user_privilege FROM users WHERE passcode=:passcode", passcode= passcode)
    
    if rows:
        user= {
            'name': rows[0]['name'],
            'privilege': rows[0]['user_privilege']
        }
        return user
    else:
        return 1

def insert_into_plu(new_item):

    db = SQL("sqlite:///till_manager.db")
    
    rows= db.execute("SELECT item FROM plu WHERE item = :name", name= new_item['name'])

    if not rows:
        db.execute('''INSERT INTO plu (item, category, sub_category, price, cost_price, vat, stock_count) 
                VALUES(:item, :category, :sub_category, :price, :cost_price, :vat, :stock_count)''',
                item= new_item['name'],
                category= new_item['category'],
                sub_category= new_item['sub'],
                price= new_item['price'],
                cost_price= new_item['cost'],
                vat= new_item['vat'],
                stock_count= new_item['count']
                )
    else:
        db.execute(''' UPDATE plu SET item =:item, category=:category, sub_category=:sub_category, 
                price=:price, cost_price=:cost_price, vat=:vat,stock_count=:stock_count WHERE item=:item''',
                item= new_item['name'],
                category= new_item['category'],
                sub_category= new_item['sub'],
                price= new_item['price'],
                cost_price= new_item['cost'],
                vat= new_item['vat'],
                stock_count= new_item['count']
                )  

def show_item_list():

    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT item FROM plu")

    item_list = []
    for row in rows:
        item_list.append(row['item'])
    
    return item_list

def show_users_list():
    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT name FROM users")

    users_list = []
    for row in rows:
        users_list.append(row['name'])
    return users_list
    
def populate_users_field(name):
    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT * FROM users WHERE name=:name",name=name)
    user={}
    for row in rows:
        user = {
            'name': row['name'],
            'passcode': row['passcode'],
            'user_type': row['user_privilege']
        } 
    return user   
def populate_plu_fields(name):

    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT * FROM plu WHERE item=:item",item=name)
    item = {}
    for row in rows:
        item = {
            'id':row['id'],
            'name': row['item'],
            'category': row['category'],
            'sub': row['sub_category'],
            'price': row['price'],
            'cost': row['cost_price'],
            'vat': row['vat'],
            'count': row['stock_count']
         }
    return item

def get_item(item_name):
    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT * FROM plu WHERE item=:item_name",item_name=item_name)
    for row in rows:
        item = {
            'name': row['item'],
            'price': row['price'],
            'vat': row['vat']
        }
    return item


def get_items_by_sub_cat(sub):
    db = SQL("sqlite:///till_manager.db")

    rows = db.execute("SELECT item FROM plu WHERE sub_category=:sub", sub=sub)
    categories = []
    
    for row in rows:
        categories.append(row['item'])
    
    return categories

def delete_user(name):
    db = SQL("sqlite:///till_manager.db")

    db.execute("DELETE FROM users WHERE name=:item", item=name)


def delete_item(name):

    db = SQL("sqlite:///till_manager.db")

    db.execute("DELETE FROM plu WHERE item=:item", item=name)





#========================== end of items and users database ==================================#





#========================== start of buttons database ========================================#

def init_buttons_database():

    open('buttons.db', 'a').close()
    db = SQL('sqlite:///buttons.db')

    db.execute(""" CREATE TABLE IF NOT EXISTS main (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        style TEXT NOT NULL,
        width INTEGER,
        height INTEGER,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL) """)

    db.execute(""" CREATE TABLE IF NOT EXISTS sub (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        main INTEGER NOT NULL,
        style TEXT NOT NULL,
        width INTEGER,
        height INTEGER,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL) """)

    db.execute(""" CREATE TABLE IF NOT EXISTS item (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        main INTEGER NOT NULL,
        sub INTEGER NOT NULL,
        style TEXT NOT NULL,
        width INTEGER,
        height INTEGER,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL) """)

def save_menu_button(button):

    db = SQL('sqlite:///buttons.db')

    db.execute("""INSERT INTO main (name, style, width,height,x,y ) VALUES(:name, :style, :width,:height,:x, :y)""",
            name= button['name'],
            style=button['style'],
            width=button['width'],
            height=button['height'],
            x=button['x'],
            y=button['y'])

def save_sub_button(button):

    db = SQL('sqlite:///buttons.db')

    db.execute("""INSERT INTO sub (name,main, style, width,height,x,y ) VALUES(:name,:main, :style, :width,:height,:x, :y)""",
            name= button['name'],
            main=button['main'],
            style=button['style'],
            width=button['width'],
            height=button['height'],
            x=button['x'],
            y=button['y'])

def save_item_buttons(button):
    
    db = SQL('sqlite:///buttons.db')

    db.execute("""INSERT INTO item (name,main,sub, style, width,height,x,y ) VALUES(:name,:main,:sub, :style, :width,:height,:x, :y)""",
            name= button['name'],
            main=button['main'],
            sub=button['sub'],
            style=button['style'],
            width=button['width'],
            height=button['height'],
            x=button['x'],
            y=button['y'])


def get_top_buttons():
    db = SQL('sqlite:///buttons.db')
    buttons=[]
    
    rows = db.execute("SELECT * FROM main",)
    for row in rows:
        button = {
            'name':row['name'],
            'style':row['style'],
            'width': row['width'],
            'height':row['height'],
            'x':row['x'],
            'y':row['y']
        }
        buttons.append(button)
    return buttons
def get_sub_buttons(index):
    db = SQL('sqlite:///buttons.db')
    buttons=[]
    rows = db.execute("SELECT * FROM sub WHERE main=:main",main=index)
    for row in rows:
        button = {
            'name':row['name'],
            'main':row['main'],
            'style':row['style'],
            'width': row['width'],
            'height':row['height'],
            'x':row['x'],
            'y':row['y']
        }
        buttons.append(button)
    return buttons
def get_item_buttons(main,index):
    db = SQL('sqlite:///buttons.db')
    buttons=[]
    rows = db.execute("SELECT * FROM item WHERE main=:main AND sub=:sub",main=main, sub=index)
    for row in rows:
        button = {
            'name':row['name'],
            'main':row['main'],
            'sub':row['sub'],
            'style':row['style'],
            'width': row['width'],
            'height':row['height'],
            'x':row['x'],
            'y':row['y']
        }
        buttons.append(button)
    return buttons
def delete_button(table,name,index=None):
    db = SQL('sqlite:///buttons.db')
    if index != None: 
        db.execute("DELETE FROM :table WHERE name=:name AND main=:main", table=table, name=name,main=index)
    else:
        db.execute("DELETE FROM :table WHERE name=:name", table=table, name=name)


#================================= end of buttons database =============================#





#================================= starts of map database ==============================#


def inint_tables_database():
    open('tables.db', 'a').close()
    db = SQL('sqlite:///tables.db')

    db.execute(""" CREATE TABLE IF NOT EXISTS floors (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        style TEXT NOT NULL,
        width INTEGER,
        height INTEGER,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL) """)

    db.execute(""" CREATE TABLE IF NOT EXISTS map (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        floor TEXT NOT NULL,
        style TEXT NOT NULL,
        width INTEGER,
        height INTEGER,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL) """)


#------------------------------- STARTS OF FLOORS TABLE ---------------------------#


def save_floor(button):
    db = SQL('sqlite:///tables.db')

    db.execute("""INSERT INTO floors (name,style,width,height,x,y) VALUES(:name,:style,:width,:height,:x,:y)""",
                name=button['name'],
                style=button['style'],
                width=button['width'],
                height=button['height'],
                x=button['x'],
                y=button['y']
                )

def get_floors():
    db = SQL('sqlite:///tables.db')
    rows = db.execute("SELECT * FROM floors")
    floor_list = []
    for row in rows:
        floor = {
            'name':row['name'],
            'style':row['style'],
            'width': row['width'],
            'height':row['height'],
            'x':row['x'],
            'y':row['y']
        }
        floor_list.append(floor)
    return floor_list

def delete_floor(floor):
    db = SQL('sqlite:///tables.db')

    db.execute("DELETE FROM floors WHERE name=:name",name=floor)

#------------------------------ END OF FLOOR TABLE -----------------------------#

#----------------------------- STARTS OF MAP TABLE -----------------------------#

def get_tables(floor):
    db = SQL('sqlite:///tables.db')
    rows = db.execute("SELECT * FROM map WHERE floor=:floor",floor= floor)
    table_list = []
    for row in rows:
        table = {
            'name':row['name'],
            'floor':row['floor'],
            'style':row['style'],
            'width': row['width'],
            'height':row['height'],
            'x':row['x'],
            'y':row['y']
        }
        table_list.append(table)
    return table_list

def save_tables(table):
    db = SQL('sqlite:///tables.db')

    db.execute("""INSERT INTO map (name,floor,style,width,height,x,y) VALUES(:name,:floor,:style,:width,:height,:x,:y)""",
                name=table['name'],
                floor=table['floor'],
                style=table['style'],
                width=table['width'],
                height=table['height'],
                x=table['x'],
                y=table['y']
                )
def delete_table(floor,table):
    db = SQL('sqlite:///tables.db')

    db.execute("DELETE FROM map WHERE floor=:floor AND name=:name",floor=floor,name=table)


#------------------------------ END OF MAP TABLE ------------------#

#------------------------------STARTS OF BILLS --------------------#


def inint_bills_database():
    open('bills.db', 'a').close()
    db = SQL('sqlite:///bills.db')

    db.execute(""" CREATE TABLE IF NOT EXISTS open (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        tab TEXT NOT NULL,
        qty TEXT,
        item TEXT NOT NULL,
        price TEXT)
        """)
    db.execute(""" CREATE TABLE IF NOT EXISTS closed (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        tab TEXT NOT NULL,
        qty TEXT,
        item TEXT NOT NULL,
        price TEXT,
        sub_total TEXT NOT NULL,
        service TEXT NOT NULL,
        total TEXT NOT NULL,
        closed TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
        """)
def save_tab(tab):
    db = SQL('sqlite:///bills.db')
    db.execute("DELETE FROM open WHERE tab=:tab AND item=:item",tab=tab['tab'],item=tab['item'])

    db.execute("""INSERT INTO open (tab, qty, item, price) VALUES (:tab, :qty, :item, :price)""",
            tab=tab['tab'],
            qty=tab['qty'],
            item=tab['item'],
            price=tab['price'])

def delete_items_from_tab(tab,item):
    db = SQL('sqlite:///bills.db')

    db.execute("DELETE FROM open WHERE tab=:tab AND item=:item",tab=tab,item=item)

def get_tab(tbl_num):
    db = SQL('sqlite:///bills.db')
    tabs= []
    rows = db.execute("SELECT * FROM open WHERE tab=:tab",tab=tbl_num)
    for row in rows:
        tab = {
            'qty':row['qty'],
            'item':row['item'],
            'price':row['price']
        }
        tabs.append(tab)
    return tabs

def save_closed_tab(tab):
    db = SQL('sqlite:///bills.db')
    try:
        db.execute("""INSERT INTO closed (user,tab,qty,item,price,sub_total,service,total)
                VALUES (:user,:tab,:qty,:item,:price,:sub_total,:service,:total)""",
                user=tab['user'],
                tab=tab['tab'],
                qty=tab['qty'],
                item=tab['item'],
                price=tab['price'],
                sub_total=tab['sub'],
                service=tab['service'],
                total=tab['tot'])
    except:
        return
            
def get_closed():
    db = SQL('sqlite:///bills.db')

    rows = db.execute("SELECT * FROM closed")
    tabs =[]
    for row in rows:
        tab = {
            'user':row['user'],
            'tab': row['tab'],
            'qty': row['qty'],
            'item':row['item'],
            'price':row['price'],
            'sub':row['sub_total'],
            'service':row['service'],
            'tot':row['total'],
            'time':row['closed']
        }
        tabs.append(tab)
    return tabs
def delete_tab_from_opens(tab):
    db = SQL('sqlite:///bills.db')

    db.execute("DELETE FROM open WHERE tab=:tab",tab=tab)








if __name__ == "__main__":
    init_database()
    init_buttons_database()
    get_user_data('0000')
    x = populate_plu_fields('orata')
    user={
        'name':'aaaa',
        'passcode':'223',
    }
    update_users(user)
    print(x)