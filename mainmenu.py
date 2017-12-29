import os
from Tkinter import *
from tkFileDialog   import *
import tkMessageBox
from PIL import ImageTk,Image

def About():
    tkMessageBox.showinfo('About Us','For support contact Venkat Jagaduri(IT Head) and Mohan Sha')

def createCallBack():
    os.system('python createtbl.py')
    tkMessageBox.showinfo( "Alert", "Executed Create Table")

def imxlsCallBack():
    os.system('python 1.importdata.py')
    tkMessageBox.showinfo( "Alert", "Imported XLS Data")

def genCallBack():
    os.system('python 2.make_att_record.py')
    os.system('python 3.make_att_report.py')
    tkMessageBox.showinfo( "Alert", "Generated Final Attendance")

def checkCallBack():
    os.system('python check.py')

def checkdbCallBack():
    os.system('python checkdb.py')

def checkcfgCallBack():
    os.system('python checkcfg.py')

def checkhraCallBack():
    os.system('python checkhra.py')
    
def holidayCallBack():
    os.system('python holiday.py')
    tkMessageBox.showinfo( "Alert", "Executed Holiday")

def calendarCallBack():
    os.system('python load_calendar.py')
    tkMessageBox.showinfo( "Alert", "Executed Calendar")

def imcsvCallBack():
    os.system('python 1.import_csvdata.py')
    tkMessageBox.showinfo( "Alert", "Imported CSV Data")

def cattCallBack():
    os.system('python 4.calendar_att.py')
    tkMessageBox.showinfo( "Alert", "Updated WeekOff")

def hattCallBack():
    os.system('python 5.holiday_att.py')
    tkMessageBox.showinfo( "Alert", "Updated Holiday ")

def emailCallBack():
    os.system('python 6.email_att.py')
    tkMessageBox.showinfo( "Alert", "Email(s) Sent")

def exportCallBack():
    os.system('python 7.export.py')
    tkMessageBox.showinfo( "Alert", "Exported")

def backupCallBack():
    os.system('backup.bat')
    tkMessageBox.showinfo( "Alert", "Backup successful")

def truncateCallBack():
    os.system('python 8.deleteall.py')
    tkMessageBox.showinfo( "Alert", "Deleted")

def archiveCallBack():
    os.system('python 9.1archive.py')
    tkMessageBox.showinfo( "Alert", "Archived")

def deleteCallBack():
    os.system('python 10.delete.py')
    tkMessageBox.showinfo( "Alert", "Deleted")

def deletehraCallBack():
    os.system('python 11.deleteinhra.py')
    tkMessageBox.showinfo( "Alert", "Deleted")

root = Tk()

canvas = Canvas(root, width = 300, height = 300)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("logo.png"))  
canvas.create_image(45, 50, anchor=NW, image=img)  

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Check Config", command=checkcfgCallBack)
filemenu.add_command(label="Check DB", command=checkCallBack)
filemenu.add_command(label="Check Archive", command=checkhraCallBack)
filemenu.add_separator()
filemenu.add_command(label="Show Run/Backups", command=checkdbCallBack)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

mastermenu = Menu(menu)
menu.add_cascade(label="Master", menu=mastermenu)
mastermenu.add_command(label="Create Table", command=createCallBack)
mastermenu.add_command(label="Holiday", command=holidayCallBack)
mastermenu.add_command(label="Calendar", command=calendarCallBack)

transmenu = Menu(menu)
menu.add_cascade(label="Transaction", menu=transmenu)
transmenu.add_command(label="1. Import Data from XLS", command=imxlsCallBack)
transmenu.add_command(label="1. Import Data from CSV", command=imcsvCallBack)
transmenu.add_command(label="2. Generate Attendance", command=genCallBack)
transmenu.add_command(label="3. Updated WeekOff", command=cattCallBack)
transmenu.add_command(label="4. Update Holiday", command=hattCallBack)
transmenu.add_command(label="5. Mail Merge", command=emailCallBack)
transmenu.add_command(label="6. Export", command=exportCallBack)

adminmenu = Menu(menu)
menu.add_cascade(label="Admin", menu=adminmenu)
adminmenu.add_command(label="Backup", command=backupCallBack)
adminmenu.add_command(label="Delete All", command=truncateCallBack)
adminmenu.add_command(label="Archive", command=archiveCallBack)
adminmenu.add_command(label="Delete Table", command=deleteCallBack)
adminmenu.add_command(label="Delete In HRA", command=deletehraCallBack)


helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About Us", command=About)

root.title("Employee Attendance Manager")
root.geometry("450x180")
mainloop()
