#import libraries
import MySQLdb
import ConfigParser

#reading config file
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Establish a MySQL connection
database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                               user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

# Get the cursor, which is used to traverse the database, line by line
delete_cursor = database.cursor()

#declare queries
ac_query="TRUNCATE TABLE ac_data;"
att_rep_query="TRUNCATE TABLE att_report;"
att_sta_query="TRUNCATE TABLE att_stage01;"
erp_query="TRUNCATE TABLE erp_report;" 
mob_query="TRUNCATE TABLE mob_data;"
email_query="TRUNCATE TABLE email;"

#execute queries
delete_cursor.execute(ac_query)
delete_cursor.execute(att_rep_query)
delete_cursor.execute(att_sta_query)
delete_cursor.execute(erp_query)
delete_cursor.execute(mob_query)
delete_cursor.execute(email_query)

# Close the cursor
delete_cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print "\nAll Done" 
print "\nI have deleted all rows from \
\nac_data\natt_report\natt_stage01\nerp_report\nmob_data\nemail\nexcept calendar & holiday !!"
