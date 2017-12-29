#import libraries
import MySQLdb
from calendar import monthrange
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
att_read_cursor = database.cursor()
insert_cursor = database.cursor()
erp_update_cursor = database.cursor()
erp_read_cursor = database.cursor()


tbl1_name="holiday"
tbl2_name="att_report"
tbl3_name="erp_report"

ic=0

# Create the Select sql query
hol_query = """SELECT * FROM `"""+tbl1_name+"""`;"""

ctr=0
# Execute sql Query
hol_read_cursor.execute(hol_query)
hol_count = hol_read_cursor.rowcount

hol_row = hol_read_cursor.fetchone()
#for each holiday update the corresponding records
while hol_row is not None:
    dt1 = datetime.strptime(hol_row[0], '%d-%b-%Y')
    #print str(dt1)
    #print str(datetime.strftime(dt1,'%d-%m-%Y'))
    hol_date = str(datetime.strftime(dt1,'%d-%m-%Y'))
    #print type(hol_date)
    att_query = """SELECT * FROM `"""+tbl2_name+"""` WHERE `Date`="""+"'"+hol_date+"'"
    print att_query

    att_read_cursor.execute(att_query)
    att_count = att_read_cursor.rowcount
    att_row = att_read_cursor.fetchall()
    if att_count > 0:
        for i in range(0,att_count-1):
            print att_row[i][0]
            erp_read_query = """SELECT Employee_Location FROM `"""+tbl3_name+"""` WHERE `E_code`="""+att_row[i][0]
            print erp_read_query
            erp_read_cursor.execute(erp_read_query)
            erp_count = erp_read_cursor.rowcount
            erp_row = erp_read_cursor.fetchone()
            print erp_row[0] +" ||| "+hol_row[2]
            if erp_row[0] in hol_row[2]:
                
                if att_row[i][2] =='A':
                    erp_update_query = """UPDATE `"""+tbl2_name+"""` SET `Leave_status`='PH' WHERE `ID`="""+"'"+att_row[i][0]+"'"+""" AND `Date`="""+"'"+hol_date+"'"
                    print erp_update_query
                    erp_update_cursor.execute(erp_update_query)
                    ctr=ctr+1
                    print "updated Leave status = PH"
            else:
                print "location Not in List"
        
    else:
        print "No record for "+str(hol_date)
    hol_row = hol_read_cursor.fetchone()    



# Close the cursor
hol_read_cursor.close()
insert_cursor.close()
att_read_cursor.close()
erp_update_cursor.close()
#xexit()
# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print "All Done!"
print "I just Updated "  + str(ctr) + " rows to MySQL!"