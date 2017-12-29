#import libraries
import MySQLdb
from datetime import datetime , time, tzinfo, timedelta
import ConfigParser
from Tkinter import *
from tkMessageBox import *

def exec_calatt(*event):
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    #function for left substring
    def left(s, amount = 1, substring = ""):
        if (substring == ""):
            return s[:amount]
        else:
            if (len(substring) > amount):
                substring = substring[:amount]
            return substring + s[:-amount]

    #function for right substring
    def right(s, amount = 1, substring = ""):
        if (substring == ""):
            return s[-amount:]
        else:
            if (len(substring) > amount):
                substring = substring[:amount]
            return s[:-amount] + substring
    
    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    # Get the cursor, which is used to traverse the database, line by line
    cal_read_cursor = database.cursor()
    att_read_cursor = database.cursor()
    erp_update_cursor = database.cursor()
    erp_read_cursor = database.cursor()


    tbl1_name="calendar"
    tbl2_name="att_report"
    tbl3_name="erp_report"

    #input to calculate the saturday and sunday of each year
    #yr = raw_input("Enter year of calendar: ")
    yr=int(inp_yr.get())
    startdate = datetime(int(yr),int(1),1)
    #print startdate.strftime('%Y-%m-%d')
    ic=0
    ctr=0

    # Create the Select sql query
    cal_query = "UPDATE att_report SET Leave_status='WO' WHERE (DAYOFWEEK(STR_TO_DATE(Date, '%d-%m-%Y')) = 7 or DAYOFWEEK(STR_TO_DATE(Date, '%d-%m-%Y')) = 1) and Leave_status in ('A')"

    print cal_query
    # Execute sql Query
    cal_read_cursor.execute(cal_query)

 #   cal_count = cal_read_cursor.rowcount

#    cal_row = cal_read_cursor.fetchone()
#    while cal_row is not None:
    #    cal_date = datetime.strptime(cal_row[0],'%d-%m-%Y')
        #print str(type(cal_date))
    #    c_date = datetime.strftime(cal_date,'%d-%m-%Y')
        #print c_date
    #    att_query = """SELECT * FROM `"""+tbl2_name+"""` WHERE `Date`="""+"'"+str(c_date)+"'"
        #print att_query

    #    att_read_cursor.execute(att_query)
     #   att_count = att_read_cursor.rowcount
    #    att_row = att_read_cursor.fetchall()
    #    if att_count > 0:
    #        for i in range(0,att_count-1):
                #print att_row[i][0]
    #            erp_read_query = """SELECT Employee_Calendar FROM `"""+tbl3_name+"""` WHERE `E_code`="""+att_row[i][0]
                #print erp_read_query
    #           erp_read_cursor.execute(erp_read_query)
    #            erp_count = erp_read_cursor.rowcount
    #            erp_row = erp_read_cursor.fetchone()
                #print erp_row[0] +" ||| "+cal_row[2]
    #            if erp_row[0] == cal_row[2]:
    #                
    #               if att_row[i][2] =="A":
    #                    erp_update_query = """UPDATE `"""+tbl2_name+"""` SET `Leave_status`='WO' WHERE `ID`="""+"'"+att_row[i][0]+"'"+""" AND `Date`="""+"'"+str(c_date)+"'"
    #                    #print erp_update_query
    #                    erp_read_cursor.execute(erp_update_query)
    #                    ctr=ctr+1
                        #print "updated Leave status = WO"
    #            else:
    #                pass
                    #print "location Not in List"
    #    else:
        #    pass
            #print "No record for "+str(c_date)
            
    #    cal_row = cal_read_cursor.fetchone()    



    # Close the cursor
    cal_read_cursor.close()
    #att_read_cursor.close()
    #erp_update_cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    # Print results
    print ""
    print "All Done!"
    #print "I just Updated "  + str(ctr) + " rows to MySQL!"
    root.destroy()

def checkYearOnly(event):
    print inp_yr.get()
    if inp_yr.get().isdigit() and int(inp_yr.get()) > 2016 and int(inp_yr.get()) < 2099:
        root.withdraw()
        exec_calatt()
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