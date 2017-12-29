#import libraries
import Tkinter
import os
import tkMessageBox
from Tkinter import *
#Tk, Button, Frame, Entry, END
top = Tk()
# Code to add widgets will go here...

#Tk.wm_iconbitmap('icon.ico')
class ABC(Frame):
    def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.parent = parent
            self.pack()
            ABC.make_widgets(self)
               
    def make_widgets(self):
            self.parent.title("Employee Attendance Manager")
#execute corresponding files
def createCallBack():
    #execfile('createtbl.py')
    os.system('python createtbl.py')
    tkMessageBox.showinfo( "Alert", "Executed Create Table")

def holidayCallBack():
    #execfile('holiday.py')
    os.system('python holiday.py')
    tkMessageBox.showinfo( "Alert", "Executed Holiday")

def calendarCallBack():
    #execfile('holiday.py')
    os.system('python load_calendar.py')
    tkMessageBox.showinfo( "Alert", "Executed Calendar")

def imxlsCallBack():
    #execfile('importdata.py')
    os.system('python 1.importdata.py')
    tkMessageBox.showinfo( "Alert", "Imported XLS Data")

def imcsvCallBack():
    #execfile('import_csvdata.py')
    os.system('python 1.import_csvdata.py')
    tkMessageBox.showinfo( "Alert", "Imported CSV Data")

def hattCallBack():
    #execfile('holiday_att.py')
    os.system('python 5.holiday_att.py')
    tkMessageBox.showinfo( "Alert", "Updated Holiday ")

def cattCallBack():
    #execfile('4.calendar_att.py')
    os.system('python 4.calendar_att.py')
    tkMessageBox.showinfo( "Alert", "Updated WeekOff")

def makeattCallBack():
    #execfile('2.make_att_record.py')
    os.system('python 2.make_att_record.py')
    tkMessageBox.showinfo( "Alert", "Executed Merge All Data")

def genattCallBack():
    #execfile('3.make_att_report.py')
    os.system('python 3.make_att_report.py')
    tkMessageBox.showinfo( "Alert", "Updated Final Attendance")

def genCallBack():
    #execfile('2.make_att_record.py')
    #execfile('3.make_att_report.py')
    os.system('python 2.make_att_record.py')
    os.system('python 3.make_att_report.py')
    tkMessageBox.showinfo( "Alert", "Generated Final Attendance")

    
def backupCallBack():
    #execfile('backup.bat')
    os.system('backup.bat')
    tkMessageBox.showinfo( "Alert", "Backup successful")

def emailCallBack():
    #execfile('6.email_att.py')
    os.system('python 6.email_att.py')
    tkMessageBox.showinfo( "Alert", "Email(s) Sent")

def exportCallBack():
    #execfile('7.export.py')
    os.system('python 7.export.py')
    tkMessageBox.showinfo( "Alert", "Exported")

def truncateCallBack():
    #execfile('8.deleteall.py')
    os.system('python 8.deleteall.py')
    tkMessageBox.showinfo( "Alert", "Deleted")

def archiveCallBack():
    #execfile('9.archive.py')
    os.system('python 9.1archive.py')
    tkMessageBox.showinfo( "Alert", "Archived")

def deleteCallBack():
    #execfile('10.delete.py')
    os.system('python 10.delete.py')
    tkMessageBox.showinfo( "Alert", "Deleted")

def deletehraCallBack():
    #execfile('11.deleteinhra.py')
    os.system('python 11.deleteinhra.py')
    tkMessageBox.showinfo( "Alert", "Deleted")

#declare widgets
MTXT = Tkinter.Label(top, text="Master")
B = Tkinter.Button(top, text ="Create Table", command = createCallBack, activebackground="Green", width=20) #createtbl.py
E = Tkinter.Button(top, text ="Holiday", command = holidayCallBack, activebackground="Green", width=20) #holiday.py
H = Tkinter.Button(top, text ="Calendar", command = calendarCallBack, activebackground="Green", width=20) #load_calendar.py
TTXT = Tkinter.Label(top, text="Transaction")
C = Tkinter.Button(top, text ="1. Import Data from XLS", command = imxlsCallBack, activebackground="Green", width=20) #importdata.py
D = Tkinter.Button(top, text ="1. Import Data from CSV", command = imcsvCallBack, activebackground="Green", width=20) #import_csvdata.py
P = Tkinter.Button(top, text ="2. Generate Attendance ", command = genCallBack, activebackground="Green", width=20) #2.make_att_record.py  3.make_att_report.py
#L = Tkinter.Button(top, text ="2. Merge Attend Sources", command = makeattCallBack, activebackground="Green", width=20) #2.make_att_record.py
#M = Tkinter.Button(top, text ="3. Generate Attendance", command = genattCallBack, activebackground="Green", width=20) #3.make_att_report30.py
I = Tkinter.Button(top, text ="3. Updated WeekOff", command = cattCallBack, activebackground="Green", width=20) #calendar_att.py
F = Tkinter.Button(top, text ="4. Update Holiday", command = hattCallBack, activebackground="Green", width=20) #holiday_att.py
J = Tkinter.Button(top, text ="5. Mail Merge", command = emailCallBack, activebackground="Green", width=20) #6.email_att30.py
K = Tkinter.Button(top, text ="6. Export", command = exportCallBack, activebackground="Green", width=20) #7.export.py
ATXT = Tkinter.Label(top, text="Administrator")
G = Tkinter.Button(top, text ="Backup ", command = backupCallBack, activebackground="Green", width=20) #backup.bat
N = Tkinter.Button(top, text ="Delete All ", command = truncateCallBack, activebackground="Green", width=20) #8.deleteall.py
O = Tkinter.Button(top, text ="Archive ", command = archiveCallBack, activebackground="Green", width=20) #9.1archive.py
Q = Tkinter.Button(top, text ="Delete Table ", command = deleteCallBack, activebackground="Green", width=20) #10.delete.py
R = Tkinter.Button(top, text ="Delete In HRA ", command = deletehraCallBack, activebackground="Green", width=20) #11.deleteinhra.py

#order to display the widgets
MTXT.pack(pady=6)
B.pack(side=Tkinter.TOP)
E.pack(pady=8)
H.pack()
TTXT.pack(pady=8)
C.pack(pady=8)
D.pack(pady=8)
P.pack(pady=8)
#L.pack(pady=8)
#M.pack(pady=8)
I.pack(pady=8)
F.pack(pady=8)
J.pack(pady=8)
K.pack(pady=8)
ATXT.pack(pady=8)
G.pack(pady=8) 
N.pack(pady=8)
O.pack(pady=8)
Q.pack(pady=8)
R.pack(pady=8)

#start the display
top.title("Employee Attendance Manager")
top.geometry("200x710")
top.mainloop()