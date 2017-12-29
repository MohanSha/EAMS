#import libraries
import MySQLdb
import ConfigParser

#reading config file
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Establish a MySQL connection
database = MySQLdb.connect (host=Config.get("hradb","host"), port=int(Config.get("hradb","port")),
                               user=Config.get("hradb","user"), passwd=Config.get("hradb","password"), db=Config.get("hradb","db"))

# Get the cursor, which is used to traverse the database, line by line
clone_cursor = database.cursor()


# Create the sql queries
ac_query="INSERT INTO hra.ac_data (SELECT * FROM hr.ac_data);"
att_rep_query="INSERT INTO hra.att_report (SELECT * FROM hr.att_report);"
att_sta_query="INSERT INTO hra.att_stage01 (SELECT * FROM hr.att_stage01);"
cal_query="INSERT INTO hra.calendar (SELECT * FROM hr.calendar);"
email_tr_query="TRUNCATE TABLE email;"
email_query="INSERT INTO hra.email (SELECT * FROM hr.email);"
erp_tr_query="TRUNCATE TABLE erp_report;"
erp_rep_query="INSERT INTO hra.erp_report (SELECT * FROM hr.erp_report);"
hol_query="INSERT INTO hra.holiday (SELECT * FROM hr.holiday);"
mob_query="INSERT INTO hra.mob_data (SELECT * FROM hr.mob_data);"

#execute queries
clone_cursor.execute(ac_query)
clone_cursor.execute(att_rep_query)
clone_cursor.execute(att_sta_query)
clone_cursor.execute(email_tr_query)
clone_cursor.execute(email_query)
clone_cursor.execute(erp_tr_query)
clone_cursor.execute(erp_rep_query)
clone_cursor.execute(mob_query)

# Close the cursor
clone_cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print "\nAll Done" 
print "\nAttendance has been archived !!"