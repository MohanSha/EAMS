#import libraries
import csv
import xlrd
import MySQLdb
from array import *
import ConfigParser
import os
from tkFileDialog import *
from Tkinter import *
import tkMessageBox

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

root = Tk()
root.withdraw()

# Open the workbook and define the worksheet
#filename = raw_input('Enter Table Excel Filename [tablename.xls]: ')
askfile = askopenfilename(filetypes=[("Excel files","*.csv")])
#print os.path.split(askfile)[1]
#exit()
filename = os.path.split(askfile)[1]
book = xlrd.open_workbook(filename)
sheet = book.sheet_by_name("Sheet1")
tbl_filename = left(filename,(len(filename)-4))
book_tbl = xlrd.open_workbook(tbl_filename+"_tbl.xls")
sheet_tbl = book_tbl.sheet_by_name("Sheet1")


# Establish a MySQL connection
database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                               user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query
queryBOL = """INSERT INTO `"""+tbl_filename+"""`("""
column_list = ""
value_list = ""
print "sheet_tbl.nrows = "+str(sheet_tbl.nrows)
for cname in range(1, sheet_tbl.nrows):
    if cname==sheet_tbl.nrows-1 :
        column_list = column_list + "`"+sheet_tbl.cell(cname,0).value+"`"
        value_list = value_list +"%s"
    else :
        column_list = column_list + "`"+sheet_tbl.cell(cname,0).value+"`, "
        value_list = value_list +"%s,"

#print column_list
#print value_list

query2 = column_list+""") VALUES ("""+value_list
queryEOL = """);"""
#construct sql query for insert
query = queryBOL+query2+queryEOL
print query

select_qry = """select * from """+tbl_filename+""" ;"""

#read each row and coloumn from input excel
csv_data = csv.reader(file(filename))
row_count = 0
for row in csv_data:
    if row_count == 0 :
        pass
    else:
        cursor.execute(query, row)
    row_count = row_count+1

'''
# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
inputrow = []
for r in range(1, sheet.nrows):
#   if r > 50 :
#       break
#print str(r)+" Out of "+str(sheet.nrows)
    for c in range(0, sheet.ncols):
        inputrow.append(str(sheet.cell(r,c).value))
    #print inputrow

    # Execute sql Query
    cursor.execute(query, inputrow)
    inputrow = []

#Run select_qry to check the data uploaded
#cursor.execute(select_qry)
#result = cursor.fetchall()
#print result
csv_data = csv.reader(file(filename))   
row_count = sum(1 for row in csv_data)
'''

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
#columns = str(sheet_tbl.ncols)
columns = str(sheet_tbl.nrows)
print "I just imported " + columns + " columns and " + str(row_count) + " rows to MySQL!"

mainloop()
