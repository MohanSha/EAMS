import ldap
import getpass
import os
from Tkinter import *
from tkMessageBox import *
import MySQLdb
import ConfigParser

def clear_widget(event):
 
    # will clear out any entry boxes defined below when the user shifts
    # focus to the widgets defined below
    if username_box == main.focus_get() and username_box.get() == 'Enter Username':
        username_box.delete(0, END)
    elif password_box == password_box.focus_get() and password_box.get() == '     ':
        password_box.delete(0, END)
 
def repopulate_defaults(event):
 
    # will repopulate the default text previously inside the entry boxes defined below if
    # the user does not put anything in while focused and changes focus to another widget
    if username_box != main.focus_get() and username_box.get() == '':
        username_box.insert(0, 'Enter Username')
    elif password_box != main.focus_get() and password_box.get() == '':
        password_box.insert(0, '     ')
 
def login(*event):
 
    # Able to be called from a key binding or a button click because of the '*event'
    auth()
    #print 'Username: ' + username_box.get()
    #print 'Password: ' + password_box.get()
 # main.destroy()
    # If I wanted I could also pass the username and password I got above to another 
    # function from here.

def auth():
    conn=ldap.initialize('ldap://sathyam.realimage.co.in')
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)
    username = username_box.get()
    username+= "@qubecinema.com" 
    password = password_box.get()
    try:
        conn.simple_bind_s(username,password)
        main.withdraw()
        basedn = "dc=realimage,dc=co,dc=in"
        searchScope = ldap.SCOPE_SUBTREE
        searchFilter = "(sAMAccountName="+username_box.get()+")"
        searchAttribute = ['employeeid','samaccountname','displayname']
        ldap_res = conn.search_s(basedn,searchScope, searchFilter, searchAttribute)
        displayname = ldap_res[0][1]['displayName'][0]
        domainid = ldap_res[0][1]["sAMAccountName"][0]
        if 'employeeID' in ldap_res[0][1]:
            emplid = ldap_res[0][1]['employeeID'][0]
        else:
            emplid = domainid
        
        #reading config file
        Config = ConfigParser.ConfigParser()
        Config.read("config.ini")
        
        # Establish a MySQL connection
        database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))
        #get cursor to traverse 
        role_cursor = database.cursor()
        
        role_query="SELECT DISTINCT Role_id FROM user_role where Emp_code='"+emplid+"'"

        #excute query
        role_cursor.execute(role_query)

        role_row = role_cursor.fetchone()
        if role_row is not None:
            print role_row[0]
            showinfo('Success', 'Access granted ')
            main.destroy()
            # Close the cursor
            role_cursor.close()
            # Commit the transaction
            database.commit()
            # Close the database connection
            database.close()
            os.system('python mainmenu.py')
        else:
            showerror('Failure', 'You dont have the required access')
            main.destroy()

    except ldap.LDAPError, e:
        showerror('Auth Error', e)
        username_box.delete(0, END)
        password_box.delete(0, END)
        username_box.focus()
        main.mainloop()


# creates the main window object, defines its name, and default size
main = Tk()
main.title('Authentication Box')
#main.geometry('225x150')
 
w = 225 # width for the Tk root
h = 150 # height for the Tk root
# get screen width and height
ws = main.winfo_screenwidth() # width of the screen
hs = main.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
# set the dimensions of the screen 
# and where it is placed
main.geometry('%dx%d+%d+%d' % (w, h, x, y))

# defines a grid 50 x 50 cells in the main window
rows = 0
while rows < 10:
    main.rowconfigure(rows, weight=1)
    main.columnconfigure(rows, weight=1)
    rows += 1
 
Label(main, text="Username").grid(row=1,column=2)
# adds username entry widget and defines its properties
username_box = Entry(main)
username_box.insert(0, 'Enter Username')
username_box.bind("<FocusIn>", clear_widget)
username_box.bind('<FocusOut>', repopulate_defaults)
username_box.grid(row=1, column=5, sticky='NS')
 
Label(main, text="Password").grid(row=2,column=2)
# adds password entry widget and defines its properties
password_box = Entry(main, show='*')
password_box.insert(0, '     ')
password_box.bind("<FocusIn>", clear_widget)
password_box.bind('<FocusOut>', repopulate_defaults)
password_box.bind('<Return>', login)
password_box.grid(row=2, column=5, sticky='NS')
 
 
# adds login button and defines its properties
login_btn = Button(main, text='Login', command=login)
login_btn.bind('<Return>', login)
login_btn.grid(row=4, column=5, sticky='NESW')
 
main.mainloop()