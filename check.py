#import libraries
import MySQLdb
import ConfigParser
import tkMessageBox
import Tkinter as tk

root = tk.Tk()
root.withdraw()

#reading config file
Config = ConfigParser.ConfigParser()
Config.read("config.ini")

# Establish a MySQL connection
database = MySQLdb.connect (host=Config.get("attenddb","host"), port=int(Config.get("attenddb","port")),
                               user=Config.get("attenddb","user"), passwd=Config.get("attenddb","password"), db=Config.get("attenddb","db"))

#get cursor to traverse 
count_cursor = database.cursor()

#create sql query
count_query="SELECT TABLE_NAME, TABLE_ROWS FROM `information_schema`.`tables` WHERE `table_schema` = 'hr'"

#excute query
count_cursor.execute(count_query)

count_row = count_cursor.fetchone()

msg01=''

while count_row is not None:
    msg01+=str(count_row[0])+" ===> "+str(count_row[1])+"\n"
    count_row = count_cursor.fetchone()

tkMessageBox.showinfo("Info",msg01)

# Close the cursor
count_cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()
