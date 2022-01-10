# coding=utf-8
"""Performs face detection in realtime.

Based on code from https://github.com/shanren7/real_time_face_recognition
"""
# MIT License
#
# Copyright (c) 2017 François Gervais
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Modify by nkloi@hcmut.edu.vn
# 3/2020

import sys
import time
import cv2
import os
import pandas as pd
import datetime
from facenet.face_contrib import *
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

def detect():
  def recognize(model_checkpoint, classifier, confidence=0.7):
    frame_interval = 3  # Number of frames after which to run face detection
    fps_display_interval = 5  # seconds
    frame_rate = 0
    frame_count = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    #tt_start = time.time()
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    width = frame.shape[1]
    height = frame.shape[0]

    face_recognition = Recognition(model_checkpoint, classifier)
    start_time = time.time()
    colors = np.random.uniform(0, 255, size=(1, 3))
    col_names = ['ID', 'Name', 'Date', 'Check-in', 'Status']
    attendance = pd.DataFrame(columns=col_names)
    #tt_start = time.time()
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if (frame_count % frame_interval) == 0:
            faces = face_recognition.identify(frame)
            for i in range(len(colors), len(faces)):
                colors = np.append(colors, np.random.uniform(150, 255, size=(1, 3)), axis=0)
            # Check our current fps
            end_time = time.time()
            if (end_time - start_time) > fps_display_interval:
                frame_rate = int(frame_count / (end_time - start_time))
                start_time = time.time()
                frame_count = 0

        #Add Overlays
        df = pd.read_csv("Student_Information" + os.sep + "StudentDetails.csv")
        data_id = df['ID']
        data_name = df['Name']
        cell = len(data_name)
        seconds = 0
        global ID
        if faces is not None:
           for idx, face in enumerate(faces):
              face_bb = face.bounding_box.astype(int)
              cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)

              if face.name and face.prob:
                 if face.prob > confidence:
                    class_name = face.name
                    for x in data_name:
                        for i in range(0, cell):
                            if data_name[i] == class_name:
                                ID = data_id[i]

                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    checkin = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    class_name = str(class_name)
                    ID = str(ID)
                    stt = 'Present'
                    attendance.loc[len(attendance)] = [ID, class_name, date, checkin, stt]
                    # ---Put info into frame---
                    cv2.putText(frame, class_name, (face_bb[0], face_bb[3] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                colors[idx], thickness=2, lineType=2)
                    cv2.putText(frame, ID, (face_bb[0], face_bb[3] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                colors[idx], thickness=2, lineType=2)
                    cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[idx], thickness=1, lineType=2)
                 else:
                    class_name = 'Unknow'
                    # ---Info of frame when "Unknown"
                    cv2.putText(frame, class_name, (face_bb[0], face_bb[3] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                colors[idx], thickness=2, lineType=2)
                    cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[idx], thickness=1, lineType=2)

              cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                        thickness=2, lineType=2)

        frame_count += 1
        cv2.imshow('Recognize Face', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #tt_end = time.time()
    #seconds = tt_end - tt_start
    #tt = time.strftime("%H:%M:%S", time.gmtime(seconds))
    attendance = attendance.drop_duplicates(subset=['ID'], keep='first')
    subject_tit = sub_tx.get()
    class_period = period_tx.get()
    ts = time.time()
    date_sub = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    fileName = "Student_Attendance" + os.sep + subject_tit + "_" + date_sub +"_"+ class_period +".csv"
    #Export dataframe to csv file
    attendance.to_csv(fileName, index=False) #index = False: to hide the index of row

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

  def Check_Stu():
      recognize('models', 'models/your_model.pkl')
      messagebox.showinfo("Announcement", "The Monitoring Process Has Been Finished!")
  def delete():
      sub_tx.delete(0, END)
      period_tx.delete(0, END)

  title = Label(win, text="Student Attendance", font=("Helvetica", 22, 'bold'), bg='#FBE4C4', fg="#F85858")
  note = Label(win, text="Note:", font=("Helvetica", 12, 'italic','underline'), bg='white', fg="#F85858")
  require = Label(win, text="Please enter the name of subject and class period",
                  font=("Helvetica", 12), bg='white', fg="#4C4A49")
  require_1 = Label(win, text="before starting to run the checking process",
                  font=("Helvetica", 12), bg='white', fg="#4C4A49")

  subject = LabelFrame(win, text="Subject Title", font=("Helvetica", 12, "bold"),fg='#4C4A49',bg='white')
  period = LabelFrame(win, text="Class Period", font=("Helvetica", 12, "bold"),fg='#4C4A49',bg='white')

  sub_tx = ttk.Entry(subject, width=58)
  period_tx = ttk.Entry(period, width=58)

  button_check = ttk.Button(win, text="Start",command = Check_Stu)
  button_clear = ttk.Button(win, text="Clear Info",command = delete)
  #----Position
  title.place(x=0, y=0, width=480, height=60)
  note.place(x=50, y=75)
  require.place(x=50, y=105)
  require_1.place(x=50, y=125)
  subject.place(x=50, y=180, height=55, width=380)
  period.place(x=50, y=270, height=55, width=380)

  button_check.place(x=50, y=370)
  button_clear.place(x=150, y=370)

  sub_tx.pack()
  period_tx.pack()
if __name__ == '__main__':
      win = Tk()
      win.title('Checking Attendance')
      win.iconbitmap('icons\check_attend.ico')
      win.configure(bg='white')
      win.geometry("480x440+20+20")
      detect()
      win.mainloop()

