#import libraries
import MySQLdb
import ConfigParser
from Tkinter import *
from tkMessageBox import *

def exec_delete(*event):
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    #get cursor to traverse 
    delete_cursor = database.cursor()

    #del_tbl=raw_input("Enter table name to delete :")
    del_tbl= str(inp_tbl.get())

    #create sql query
    del_query="TRUNCATE TABLE "+del_tbl+";"

    #excute query
    delete_cursor.execute(del_query)

    # Close the cursor
    delete_cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    # Print results
    print "\nAll Done" 
    print "\nI have deleted all rows in "+del_tbl+" !!"
    emain.destroy()

def delete(event):
    exec_delete()


emain = Tk()
emain.title('Input')

Label(emain, text="Enter table name to delete : ").grid(row=1,column=2,sticky=W,pady=4)
inp_tbl = Entry(emain)
inp_tbl.grid(row=1,column=4,padx=12)
inp_tbl.bind('<Return>', delete)
inp_tbl.focus()


emain.mainloop()
