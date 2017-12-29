#import libraries
import MySQLdb
import ConfigParser
from Tkinter import *
from tkMessageBox import *

def exec_deletehra(*event):
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("hradb","host"), port=int(Config.get("hradb","port")),
                                user=Config.get("hradb","user"), passwd=Config.get("hradb","password"), db=Config.get("hradb","db"))

    #get cursor to traverse
    delete_cursor = database.cursor()

    #sd=raw_input("Enter Start Date: ")
    #ed=raw_input("Enter End Date: ")
    sd=str(inp_sd.get())
    ed=str(inp_ed.get())


    #create sql query
    hra_att_del="DELETE FROM `att_report` WHERE STR_TO_DATE(Date,'%d-%m-%Y') BETWEEN STR_TO_DATE('"+sd+"','%d-%m-%Y') AND STR_TO_DATE('"+ed+"','%d-%m-%Y')"
    print hra_att_del
    #hra_erp_del="DELETE FROM `erp_report` WHERE STR_TO_DATE(Date,'%d-%m-%Y') BETWEEN STR_TO_DATE("+sd+",'%d-%m-%Y') AND STR_TO_DATE("+sd+",'%d-%m-%Y')"

    #execute query
    delete_cursor.execute(hra_att_del)
    #delete_cursor.execute(hra_erp_del)

    # Close the cursor
    delete_cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    # Print results
    print "\nAll Done" 
    print "\nI have deleted all rows from "+sd+" to "+ed
    emain.destroy()

def delete(event):
    if inp_sd.get()!="" and inp_ed.get()!="":
        emain.withdraw()
        exec_deletehra()
        return True
    else:
        if inp_sd.get()=="":
            showerror('Error','Enter a valid date')    
            inp_sd.focus()
        else:
            showerror('Error','Enter a valid date')    
            inp_ed.focus()            
        return False



emain = Tk()
emain.title('Input')

Label(emain, text="Enter Start Date: ").grid(row=1,column=2,sticky=W,pady=4)
Label(emain, text="Enter End Date: ").grid(row=2,column=2,sticky=W,pady=4)
inp_sd = Entry(emain)
inp_sd.grid(row=1,column=4,padx=12)
inp_sd.bind('<FocusOut>')
inp_sd.focus()
inp_ed = Entry(emain)
inp_ed.grid(row=2,column=4,padx=12)
inp_ed.bind('<Return>', delete)
emain.mainloop()