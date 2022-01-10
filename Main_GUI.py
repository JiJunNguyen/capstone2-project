import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import train_image
import detection
import collect

def Students():
        os.system("py collect.py")

def TrainImages():
        train_image.align_mtcnn('your_face', 'face_align')
        train_image.train('face_align/', 'models/20180402-114759.pb', 'models/your_model.pkl')

def DetectFaces():
        os.system("py detection.py")
def SendMail():
        os.system("py automail.py")

win = Tk()
win.title('Face Recognition System')
win.iconbitmap('icons\icontitle.ico')
win.geometry("1080x720+20+20")

#-----------Backgound
back_g = PhotoImage(file= r'icons\bg.png')
#background_label = Label(win, image=fondo)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)
background = Canvas(win,width = 1080, height = 720)
background.pack(fill = "both", expand = True)

#-----------Display image
background.create_image(0, 0, image=back_g, anchor="nw")

#----------Logo
logo = PhotoImage(file= r'icons\logoedu.png')
#logo_label = Label(win, image=logo)
#logo_label.place(x=800, y=500)
background.create_image(945, 22, image=logo, anchor="nw")

#----------Title
background.create_text(140, 45, text = "Multi-Face Recognition System For Checking Attendance",font = ('Helvetica',22,'bold'),anchor = "nw")
background.create_text(355, 90, text = "----- Attendance System -----",font = ("Helvetica",22,'italic','bold'),anchor = "nw")

#----------Label frame
label_frame = PhotoImage(file= r'icons\box.png')
background.create_image(190, 180, image=label_frame , anchor="nw")
background.create_text(380, 215, text = "Control System Panel",font = ("Helvetica",23,'bold'),fill='#F85858',anchor = "nw")

#--------Icon for Button
icon1 = PhotoImage(file=r"icons\student.png")
icon2 = PhotoImage(file=r"icons\check.png")
icon3 = PhotoImage(file=r"icons\mail.png")
icon4 = PhotoImage(file=r"icons\exit.png")

#----------Button
b1 = Button(win, image = icon1, borderwidth = 0, bg='white', command = Students)
b2 = Button(win, image = icon2, borderwidth = 0, bg='white', command = DetectFaces)
b3 = Button(win, image = icon3, borderwidth = 0, bg='white', command = SendMail)
b4 = Button(win, image = icon4, borderwidth = 0, bg='white', command = win.destroy)

#title.place(x=300, y=50)
#label_frame.place(x=75, y=200)
b1.place(x=250, y=270)
b2.place(x=450, y=270)
b3.place(x=650, y=270)
b4.place(x=450, y=470)

win.mainloop()