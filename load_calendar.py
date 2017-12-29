#import libraries
import MySQLdb
import datetime as dt
from datetime import datetime , time, tzinfo, timedelta
import ConfigParser
from Tkinter import *
from tkMessageBox import *

def exec_loadcal(*event):    
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    #yr=raw_input("Enter year of calendar: ")
    yr=int(inp_yr.get())
    start_date = dt.datetime(int(yr), 1, 1)
    end_date = dt.datetime(int(yr), 12, 31)

    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    insert_cursor = database.cursor()

    tbl1_name="calendar"

    # Create the Select sql query
    query = """SELECT * FROM `"""+tbl1_name+"""`"""
    print query

    insert_count = insert_cursor.rowcount
    #print insert_count

    total_days = (end_date - start_date).days + 1 
    ctr=0

    #insert only sat and sun in calendar table
    for day_number in range(total_days):
        current_date = (start_date + dt.timedelta(days = day_number)).date()
        f=datetime.strftime(current_date,'%d-%m-%Y')
        #print current_date
        date = str(datetime.strftime(current_date,'%a'))
        if date=="Sat" or date=="Sun":
            #print date
            insert_query="""INSERT INTO `"""+tbl1_name+"""` (`cal_date`, `cal_day`, `calendar`) VALUES ('"""+str(f)+"""','"""+str(date)+"""','GENERAL')"""
            print insert_query
            # Execute sql Query
            insert_cursor.execute(insert_query)
            ctr=ctr+1

    # Close the cursor
    insert_cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    # Print results
    print ""
    print "All Done!"
    print "I just imported "  + str(ctr) + " rows to Calendar!"
    root.destroy()


def checkYearOnly(event):
    print inp_yr.get()
    if inp_yr.get().isdigit() and int(inp_yr.get()) > 2016 and int(inp_yr.get()) < 2099:
        root.withdraw()
        exec_loadcal()
        return True
    else:
        showerror('Error', 'Enter valid Input')
        inp_yr.delete(0, END)
        inp_yr.focus()
        return False

root = Tk()
root.title('Input')
Label(root, text="Enter Year: ").grid(row=2,column=2,sticky=W,pady=4)
inp_yr = Entry(root)
inp_yr.grid(row=2,column=4,padx=8)
inp_yr.bind('<Return>', checkYearOnly)
inp_yr.focus()
mainloop()