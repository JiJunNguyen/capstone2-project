import cv2
from datetime import datetime
import os
import os.path
import csv
import time
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import train_image

def collect():
  def takeImages():
     IMG_PATH = './your_face/'
     count = 150
     stu_name = name.get()
     stu_id = ID.get()
     stu_gender = gender.get()
     stu_birth = birth.get()
     file_path = os.path.join(IMG_PATH, stu_name)
     os.mkdir(file_path)
     cap = cv2.VideoCapture(0)
     cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
     cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
     messagebox.showwarning("Announcement", "Please put your face in front of the camera")
     text = "Please put your face in front of the camera"
     time.sleep(5)
     while cap.isOpened() and count:
        isSuccess, frame = cap.read()
        path = str(file_path + '/{}.jpg'.format(str(stu_name)+'_'+str(stu_id)+'_'+ str(count)))
        print(path)
        cv2.imwrite(path, frame)
        if count==100:
            messagebox.showwarning("Announcement", "Please turn right your face")
            text = 'Please turn right your face'
            time.sleep(3)
        if count==50:
            messagebox.showwarning("Announcement", "Please turn left your face")
            text = 'Please turn left your face'
            time.sleep(3)
        count -= 1
        cv2.putText(frame, str(text), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.imshow('Capture Face', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

     announ = "Images Saved for " + stu_name + " - ID: " + stu_id
     messagebox.showinfo("Announcement", announ )

     header= ["ID", "Name", "Gender", "Birth"]
     row= [stu_id, stu_name, stu_gender, stu_birth]
     if(os.path.isfile("Student_Information"+os.sep+"StudentDetails.csv")):
        with open("Student_Information"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
           writer = csv.writer(csvFile)
           writer.writerow(row)
        csvFile.close()
     else:
        with open("Student_Information"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
           writer = csv.writer(csvFile)
           writer.writerow(header)
           writer.writerow(row)
        csvFile.close()

     cap.release()
     cv2.destroyAllWindows()

  def Train_Data():
      train_image.align_mtcnn('your_face', 'face_align')
      train_image.train('face_align/', 'models/20180402-114759.pb', 'models/your_model.pkl')
      messagebox.showinfo("Announcement", "The Training Process Has Been Finished!")
  def Clear():
      name.delete(0, END)
      ID.delete(0, END)
      gender.set('')
      birth.delete(0, END)
  def Update_data():
      tree.insert('', 'end', values=(name.get(),ID.get(), gender.get(), birth.get()))

  title_mana = Label(win, text="Student Management", font=("Helvetica", 30, 'bold'), bg='#FBE4C4', fg="#F85858")
  #---------Student Info Layout----
  title_info = LabelFrame(win, text='Student Information', font=("Helvetica", 18, "bold"), fg='#33BDFF',
                          bg='white',labelanchor = 'n')

  name_lb = LabelFrame(win, text='Full Name', font=("Helvetica", 10, "bold"), fg='#4C4A49', bg='white')
  name = ttk.Entry(name_lb,  width=35)

  ID_lb = LabelFrame(win, text='ID', font=("Helvetica", 10, "bold"), fg='#4C4A49', bg='white')
  ID = ttk.Entry(ID_lb, width=35)

  gender_lb = LabelFrame(win, text="Gender", font=("Helvetica", 10, "bold"), fg='#4C4A49', bg='white')
  gender = ttk.Combobox(gender_lb, state="readonly",width=33)
  gender["values"] = ("Select Gender", "Male", "Female", "Other")

  birth_lb = LabelFrame(win, text='Birth', font=("Helvetica", 10, "bold"), fg='#4C4A49', bg='white')
  birth = ttk.Entry(birth_lb, width=35)

  #------- Set the treeview
  title_list = Label(win, text="List Of New Student", font=("Helvetica", 20,'bold'),bg='white', fg="#9C2FF5")
  style = ttk.Style()
  tree = ttk.Treeview(win, columns=('Full Name', 'ID', 'Gender', 'Birth'),style="my.Treeview", height = 21)

  #-------Set heading treeview
  tree.heading("Full Name", text="Full Name",anchor=CENTER)
  tree.heading("ID", text="ID", anchor=CENTER)
  tree.heading("Gender", text="Gender", anchor=CENTER)
  tree.heading("Birth", text="Birth", anchor=CENTER)
  style.configure('my.Treeview.Heading', font=('Helvetica', 12,'bold'))
  #-------Set column treeview
  tree.column("#0", stretch=NO, minwidth=0, width=0)
  tree.column("Full Name", width=200,anchor = CENTER)
  tree.column("ID", width=170, anchor = CENTER)
  tree.column("Gender", width=120, anchor = CENTER)
  tree.column("Birth", width=120, anchor = CENTER)
  #style.configure('my.Treeview.Column', font=('Helvetica', 12))
  # -----------Button Layout----
  button_collect = ttk.Button(win, text="Capture", command=takeImages)
  button_update = ttk.Button(win, text="Update", command=Update_data)
  button_train = ttk.Button(win, text="Training", command=Train_Data)
  button_delete = ttk.Button(win, text="Clear", command=Clear)
  button_close = ttk.Button(win, text="Close", command=win.destroy)

  #Set up postion
  #----------Position Info entry------
  title_mana.place(x=0, y=0,width = 1080,height = 80)
  title_info.place(x = 45, y = 120,width = 300,height = 491)
  name_lb.place(x=70,y=190,width=250, height = 50)
  name.pack()
  ID_lb.place(x=70,y=260,width=250, height = 50)
  ID.pack()
  gender_lb.place(x=70,y=330,width=250, height = 50)
  gender.pack()
  birth_lb.place(x=70, y=400, width=250, height=50)
  birth.pack()

  #-------Position Treeview-----
  title_list.place(x=595, y=120)
  tree.place(x=420, y=165)

  #-------Position Button ----
  button_collect.place(x=90, y=500)
  button_update.place(x=220, y=500)
  button_train.place(x=90, y=550)
  button_delete.place(x=220, y=550)
  button_close.place(x=955, y=650)
if __name__ == "__main__":
    win = Tk()
    win.title('Student Management')
    win.iconbitmap('icons\manage.ico')
    win.configure(bg='white')
    win.geometry("1080x720+20+20")
    collect()
    win.mainloop()