import tkMessageBox
import Tkinter as tk

root = tk.Tk()
root.withdraw()

#reading config file
f= open("config.ini","r")
tkMessageBox.showinfo("Info",f.read())
exit()
