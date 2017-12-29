import string
import xlrd
import MySQLdb
from array import *
import ConfigParser
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
import os

def exec_create(*event):
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")

    def left(s, amount = 1, substring = ""):
        if (substring == ""):
            return s[:amount]
        else:
            if (len(substring) > amount):
                substring = substring[:amount]
            return substring + s[:-amount]

    def right(s, amount = 1, substring = ""):
        if (substring == ""):
            return s[-amount:]
        else:
            if (len(substring) > amount):
                substring = substring[:amount]
            return s[:-amount] + substring
        
    # Open the workbook and define the worksheet
    #filename = raw_input('Enter Table Excel Filename : ')
    filename = os.path.split(askfile)[1]
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name("Sheet1")

    # Establish a MySQL connection
    database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                                user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

    # Get the cursor, which is used to traverse the database, line by line
    cursor = database.cursor()
    tablename = left(filename,(len(filename)-8))
    print tablename
    # Create the INSERT INTO sql query
    queryBOL = """CREATE TABLE """+tablename+""" ("""

    query1 = """CREATE TABLE """+tablename+""" ("""

    queryEOL = """ );"""
    #query1= """select * from attendance;"""
    # Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
    #values = array('c',[])
    inputrow = ""
    for r in range(1, sheet.nrows):
    #   if r > 50 :
    #       break
        print str(r+1)+" Out of "+str(sheet.nrows)
        if r+1 == sheet.nrows :
            print sheet.cell(r,1).value +"= last row"
            if sheet.cell(r,1).value=="INT" :
                inputrow = inputrow + sheet.cell(r,0).value+" "+sheet.cell(r,1).value
            else : 
                inputrow = inputrow + sheet.cell(r,0).value+" "+sheet.cell(r,1).value+"("+str(int(sheet.cell(r,2).value))+")"
        else :
            print sheet.cell(r,1).value+"= "+str(r)+" row"
            if sheet.cell(r,1).value=="INT" :
                inputrow = inputrow + sheet.cell(r,0).value+" "+sheet.cell(r,1).value+","
            else :
                inputrow = inputrow + sheet.cell(r,0).value+" "+sheet.cell(r,1).value+"("+str(int(sheet.cell(r,2).value))+"),"


        print inputrow
        #values = ('d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13', 'd14', 'd15', 'd16', 'd17', 'd18', 'd19', 'd20', 'd21', 'd22', 'd23', 'd24', 'd25', 'd26', 'd27', 'd28', 'd29', 'd30', 'd31')
        #print values
    print queryBOL+inputrow+queryEOL

    query = queryBOL+inputrow+queryEOL
        # Execute sql Query
    cursor.execute(query)
        #inputrow = []

    #cursor.execute(query1)
    #result = cursor.fetchall()
    #print result
    # Close the cursor
    cursor.close()

    # Commit the transaction
    database.commit()

    # Close the database connection
    database.close()

    # Print results
    print ""
    print "All Done!"
    print ""
    columns = str(sheet.ncols)
    rows = str(sheet.nrows)
    print "I just imported " + columns + " columns and " + rows + " rows to MySQL!"
    exmain.destroy()


exmain = Tk()
exmain.title('Input')
exmain.withdraw()
askfile = askopenfilename(filetypes=[("Excel files","*_tbl.xls")])
exec_create()
exmain.mainloop()
