import tkinter
from tkinter import filedialog
#initiate tinker and hide window
path = tkinter.Tk()
path.withdraw()
path.geometry('0x0+0+0')

#open file selector
path.sourceFile = filedialog.askopenfilename(parent=path,initialdir= "/", title='Please select an attendance file')
#close window after selection
path.destroy()