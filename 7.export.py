#import libraries
import MySQLdb
from calendar import monthrange
from xlsxwriter.workbook import Workbook
from datetime import datetime , time, tzinfo, timedelta
import ConfigParser
from Tkinter import *
from tkMessageBox import *

def exec_export(*event):
    #reading config file
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")


    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    att_read_cursor = database.cursor()

    #query = "SELECT * FROM %s;" % table
    query="SELECT A.ID,B.Employee_Name,B.Employee_DOJ,B.Employee_Position,B.Employee_Department,B.Employee_Grade,B.Employee_Location,B.Employee_Calendar,A.Date,A.Leave_status FROM `att_report` A,`erp_report` B WHERE A.ID=B.E_code"
    #cursor.execute(query)
    att_read_cursor.execute(query)
    att_count = att_read_cursor.rowcount
    att_row = att_read_cursor.fetchone()

    #input to calculate the total no of days in month
    #mh=int(raw_input("Enter Month: "))
    #yr=int(raw_input("Enter Year: "))
    mh=int(inp_mh.get())
    yr=int(inp_yr.get())

    startdate = datetime(yr,mh,21)
    #print startdate.strftime('%Y-%m-%d')
    no_of_days = monthrange(yr, mh)
    tday = no_of_days[1]+1

    id_list=[];
    name_list=[];
    att_date_list=[];
    dt=[];
    att_ls_list=[];
    email_list=[];
    ic=0

    #create a excel file and export ther data
    #fname = raw_input("Enter filename to export: ")
    fname = str(inp_fn.get())
    workbook = Workbook(fname+'.xlsx')
    sheet = workbook.add_worksheet()
    r=c=0
    #manually write the first row of the excel
    sheet.write(0, c, 'Employee ID')
    sheet.write(0, c+1, 'Employee Name')
    sheet.write(0, c+2, 'Employee DOJ')
    sheet.write(0, c+3, 'Employee Position')
    sheet.write(0, c+4, 'Employee Department')
    sheet.write(0, c+5, 'Employee Grade')
    sheet.write(0, c+6, 'Employee Location')
    sheet.write(0, c+7, 'Employee Calendar')
    print "\n Please wait . . ."
    #for each employee write a row the attrendance in excel
    while att_row is not None:
        #print att_row
        prev_id = att_row[0]
        prev_name = att_row[1]
        prev_doj = att_row[2]
        prev_pos = att_row[3]
        prev_dept = att_row[4]
        prev_grade = att_row[5]
        prev_loc = att_row[6]
        prev_cal = att_row[7]
        sheet.write(r+1, 0, prev_id)
        sheet.write(r+1, 1, prev_name)
        sheet.write(r+1, 2, prev_doj)
        sheet.write(r+1, 3, prev_pos)
        sheet.write(r+1, 4, prev_dept)
        sheet.write(r+1, 5, prev_grade)
        sheet.write(r+1, 6, prev_loc)
        sheet.write(r+1, 7, prev_cal)
        #c=c+2
        
        for day in range(1,tday):
            att_date_list.insert(day,att_row[8]);
            dt.insert(day,datetime.strptime(att_date_list[day-1], '%d-%m-%Y'));
            att_ls_list.insert(day,att_row[9]); 
            att_row = att_read_cursor.fetchone()
            
            if att_row is None:
                curr_id = ""
                curr_name = ""
                #curr_email = ""
            else:
                curr_id = att_row[0]
                curr_name = att_row[1]
                #curr_email = att_row[4] 
                sheet.write(r+1, c+day+7, att_ls_list[day-1])
                #if day == dt[day-1].day:
                sheet.write(0, c+day+7,datetime.strftime(dt[day-1], '%d %b'))
                #print r, c+day, att_ls_list[day-1]
                #print 0, c+day+1, dt[day-1]
                
            if curr_id != prev_id:     
                att_date_list=[]
                dt=[]
                r=r+1
                att_ls_list=[]
                ic = ic+1

    # Close the cursor
    att_read_cursor.close()

    #close the excel
    workbook.close()


    # Close the database connection
    database.close()

    # Print results
    print "\nAll Done" 
    print "\nI have exported Master.xlsx with "+str(ic)+" rows!!"
    

def checkMonthOnly(event):
    if inp_mh.get()=="" or inp_mh.get().isdigit() and int(inp_mh.get()) > 0 and int(inp_mh.get()) < 13:
        #print "corrent"
        return True
    else:
        inp_mh.delete(0, END)
        showerror('Error', 'Enter valid Input')
        inp_mh.focus()
        return False

def checkYearOnly(event):
    if inp_yr.get()=="" or inp_yr.get().isdigit() and int(inp_yr.get()) > 2016 and int(inp_yr.get()) < 2019:
        return True
    else:
        inp_yr.delete(0, END)
        showerror('Error', 'Enter valid Input')
        inp_yr.focus()
        return False

def export(event):
    exmain.withdraw()
    exec_export()
    exmain.destroy()
    
exmain = Tk()
exmain.title('Input')

Label(exmain, text="Enter Month: ").grid(row=1,column=2,sticky=W,pady=4)
Label(exmain, text="Enter Year: ").grid(row=2,column=2,sticky=W,pady=4)
Label(exmain, text="Enter filename to export: ").grid(row=3,column=2,sticky=W,pady=4)
inp_mh = Entry(exmain)
inp_mh.grid(row=1,column=4,padx=8)
inp_mh.bind('<FocusOut>', checkMonthOnly)
inp_yr = Entry(exmain)
inp_yr.grid(row=2,column=4,padx=8)
inp_yr.bind('<FocusOut>', checkYearOnly)
inp_mh.focus()
inp_fn = Entry(exmain)
inp_fn.grid(row=3,column=4,padx=8)
inp_fn.bind('<Return>', export)

exmain.mainloop()
