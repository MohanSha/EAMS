#import libraries
import MySQLdb
from datetime import datetime , time, tzinfo, timedelta
import ConfigParser

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
hol_read_cursor = database.cursor()
insert_cursor = database.cursor()

tbl1_name="holiday"

startdate = datetime(int(2017),int(1),1)
#print startdate.strftime('%Y-%m-%d')

# Create the Select sql query
hol_query = """SELECT * FROM `"""+tbl1_name+"""`;"""

# Execute sql Query
hol_read_cursor.execute(hol_query)
hol_count = hol_read_cursor.rowcount

hol_row = hol_read_cursor.fetchone()
holiday_list =[]
ic=0

#for each holiday remove leading and ending (comma),
while hol_row is not None:
    print hol_row
    hol_list = hol_row[2]
    hol_list = hol_list.split(',')
    print str(hol_list) + ">>"+str(len(hol_list))
    for i in range(0,len(hol_list)):
        k=0
        if hol_list[i] !="":
            if i == 0:
                holiday_list.insert(k,hol_list[i])
            else:
                holiday_list.insert(k,hol_list[i]+",")
            k=k+1
    str_holiday = ''.join(holiday_list)
    if right(str_holiday,1) == ",":
        str_holiday = left(str_holiday,(len(str_holiday)-1))
    str_holiday = "'"+str_holiday+"'"
    insert_query = """UPDATE `holiday` SET `city`="""+str_holiday+""" WHERE `holiday`="""+"'"+hol_row[1]+"'"
    print insert_query
    hol_list = []
    holiday_list =[]
    ic=ic+1
    insert_cursor.execute(insert_query)

    hol_row = hol_read_cursor.fetchone()

# Close the cursor
hol_read_cursor.close()
insert_cursor.close()
#xexit()
# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print "All Done!"
print "I just Updated "  + str(ic) + " rows to MySQL!"