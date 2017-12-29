#import libraries
import MySQLdb
from calendar import monthrange
from datetime import datetime , time, tzinfo, timedelta
import ConfigParser
from Tkinter import *
from tkMessageBox import *


def exec_makeatt(*event):
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    # Get the cursor, which is used to traverse the database, line by line
    mob_read_cursor = database.cursor()
    att_read_cursor = database.cursor()
    insert_cursor = database.cursor()
    erp_read_cursor = database.cursor()

    tbl1_name="mob_data"
    tbl2_name="att_stage01"
    tbl3_name="erp_report"
    tbl4_name="att_report"

    #input to calculate the days of the month
    #mh=int(raw_input("Enter Month: "))
    #yr=int(raw_input("Enter Year: "))
    mh=int(inp_mh.get())
    yr=int(inp_yr.get())
    main.withdraw()

    startdate = datetime(yr,mh,21)
    #startdate = datetime(int(2017),int(11),21)
    #print startdate.strftime('%Y-%m-%d')

    no_of_days = monthrange(yr, mh)
    tday = no_of_days[1]+1

    # Create the Select sql query
    mob_query = """SELECT * FROM `"""+tbl1_name+"""` WHERE `Employee_ID`LIKE %s;"""
    att_query = """SELECT * FROM `"""+tbl2_name+"""` WHERE `ID`LIKE %s;"""
    erp_query = """SELECT * FROM `"""+tbl3_name+"""`;"""

    ##erp_query = "SELECT * FROM "+tbl3_name+" WHERE E_code = '00382'"


    # Execute sql Query
    erp_read_cursor.execute(erp_query)
    erp_count = erp_read_cursor.rowcount

    erp_row = erp_read_cursor.fetchone()
    ic=0

    #for each emaployee in erp mark attendance either absent or present
    while erp_row is not None:
        #if erp_row[0] == "02031":
        #print erp_row
        #else:
        #    erp_row = erp_read_cursor.fetchone()
        #    continue

        att_read_cursor.execute(att_query,'%'+str(erp_row[0]))
        #att_read_cursor.execute(att_query,'%02015')
        att_row = att_read_cursor.fetchall()
        att_count = att_read_cursor.rowcount
        att_date_cr = 0 
        #if erp_row[0]=='02091':
            #print att_count
            
        mob_read_cursor.execute(mob_query,'%'+str(erp_row[0]))
        #mob_read_cursor.execute(mob_query,'%02015')
        mob_row = mob_read_cursor.fetchone()
        mob_count = mob_read_cursor.rowcount

        val_id = str(erp_row[0])
        print "\nERP ID = "+ val_id
        #print "c = "+str(erp_read_cursor.rownumber)+" erp_count: "+str(erp_count) + " att_count: "+str(att_count) + " mob_count: "+str(mob_count)
    
        #print str(erp_row)
        insert_query="" 
    
        val_LS_list=[];

        #calculate the attendance for the no of days in month 
        for day in range(1,tday):
            val_LS = ""
            mob_LS = ""
            att_LS = ""
            if mob_count > 0:
                mob_date = startdate+timedelta(days=day-1)
                mob_LS = str(mob_row[day+1])
                val_LS = mob_LS.upper()

                #print "\n\nMOB ID = "+mob_date.strftime('%Y-%m-%d') + " Day"+str(day)+" is "+val_LS    
            if att_count > 0:
                att_date = datetime.strptime(str(att_row[att_date_cr][1]), '%d/%m/%Y')
                delt = att_date-(startdate+timedelta(days=day-1))
                #print delt.days
                if delt.days == 0:
                    att_LS = str(att_row[att_date_cr][2])
                    att_date_cr=att_date_cr+1
                    if mob_count > 0:
                        if mob_LS.upper() != "A":
                            val_LS = mob_LS.upper()
                        else:
                            val_LS = att_LS.upper()
                    else:
                        val_LS = att_LS.upper()
                else:
                    #print "Date Difference: "
                    att_date = startdate+timedelta(days=day-1)
                    att_LS = ""
                
            erp_date = startdate+timedelta(days=day-1)
            erp_LS = str(erp_row[day+7])
            if erp_date < datetime.strptime(str(erp_row[2]), '%d-%b-%Y'):
                val_LS = ""
            
            if att_LS.upper() == "P":
                val_LS = att_LS.upper()            
            else:
                if val_LS =="A":
                    pass
                else:
                    if erp_date > datetime.strptime(str(erp_row[2]), '%d-%b-%Y'):
                        if val_LS =="":
                            val_LS ="A"
                    #else:
                    #    val_LS = ""
                    
            if erp_LS != "":
                val_LS = erp_LS

            #print "ATT ID = "+att_date.strftime('%Y-%m-%d') + " Day"+str(day)+" is "+att_LS
            #print "ERP ID = "+erp_date.strftime('%Y-%m-%d') + " Day"+str(day)+" is "+erp_LS

            val_LS_list.insert(day,val_LS);

            insert_query = """INSERT INTO `att_report` (`ID`, `Date`, `Leave_status`) VALUES ('"""+val_id+"""','"""+erp_date.strftime('%d-%m-%Y')+"""','"""+val_LS+"""');"""  
            #print insert_query
            ic=ic+1
            insert_cursor.execute(insert_query)

        erp_row = erp_read_cursor.fetchone()

    # Close the cursor
    mob_read_cursor.close()
    att_read_cursor.close()
    erp_read_cursor.close()
    insert_cursor.close()
    #xexit()
    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    # Print results
    print ""
    print "All Done!"
    print "I just imported "  + str(ic) + " rows to MySQL!"
    main.destroy()

def checkMonthOnly(event):
    print inp_mh.get()
    if inp_mh.get().isdigit() and int(inp_mh.get()) > 0 and int(inp_mh.get()) < 13:
        #print "corrent"
        return True
    else:
        showerror('Error', 'Enter valid Input')
        inp_mh.delete(0, END)
        inp_mh.focus()
        return False

def checkYearOnly(event):
    print inp_yr.get()
    if inp_yr.get().isdigit() and int(inp_yr.get()) > 2016 and int(inp_yr.get()) < 2099:
        exec_makeatt()
        return True
    else:
        showerror('Error', 'Enter valid Input')
        inp_yr.delete(0, END)
        inp_yr.focus()
        return False

#self.port = ttk.Entry(self, width=35, validate='key', validatecommand=vcmd)
main = Tk()
main.title('Input')

Label(main, text="Enter Month: ").grid(row=1,column=2,sticky=W,pady=4)
Label(main, text="Enter Year: ").grid(row=2,column=2,sticky=W,pady=4)
inp_mh = Entry(main)
inp_mh.grid(row=1,column=4,padx=8)
inp_mh.bind('<FocusOut>', checkMonthOnly)
inp_yr = Entry(main)
inp_yr.grid(row=2,column=4,padx=8)
inp_yr.bind('<Return>', checkYearOnly)
inp_mh.focus()

main.mainloop()