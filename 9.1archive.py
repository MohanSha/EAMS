#import libraries
import MySQLdb
import ConfigParser

#reading config file
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Establish a MySQL connection
database = MySQLdb.connect (host=Config.get("hradb","host"), port=int(Config.get("hradb","port")),
                               user=Config.get("hradb","user"), passwd=Config.get("hradb","password"), db=Config.get("hradb","db"))

database.autocommit = True
# Get the cursor, which is used to traverse the database, line by line
clone_cursor = database.cursor()

# Create the sql queries
att_rep_query="INSERT INTO hra.att_report (SELECT * FROM hr.att_report);"
erp_tr_query="TRUNCATE TABLE erp_report;"
erp_rep_query="INSERT INTO hra.erp_report (SELECT * FROM hr.erp_report);"

#execute queries
clone_cursor.execute(att_rep_query)
clone_cursor.execute(erp_tr_query)
clone_cursor.execute(erp_rep_query)


# Close the cursor
clone_cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print "\nAll Done" 
print "\nAttendance has been archived !!"