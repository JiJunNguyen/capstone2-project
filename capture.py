import cv2
from datetime import datetime
import os
import os.path
import csv
import time
import wx

def takeImages():
  IMG_PATH = './your_face/'
  count = 150
  app = wx.App()

  frame = wx.Frame(None, -1)
  frame.SetDimensions(0, 0, 200, 50)

  # Create text input
  stu_name = wx.TextEntryDialog(frame, 'Enter Full Name', 'Student Information','')
  if stu_name.ShowModal() == wx.ID_OK:
      usr_name = stu_name.GetValue()
  stu_ID = wx.TextEntryDialog(frame, 'Enter ID', 'Student Information','')
  if stu_ID.ShowModal() == wx.ID_OK:
      usr_id = stu_ID.GetValue()

  USR_PATH = os.path.join(IMG_PATH, usr_name)
  os.mkdir(USR_PATH)
  cap = cv2.VideoCapture(0)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
  text = 'Please put your face here'
  time.sleep(5)
  while cap.isOpened() and count:
      isSuccess, frame = cap.read()
      path = str(USR_PATH + '/{}.jpg'.format(str(usr_name)+'_'+str(usr_id)+'_'+ str(count)))
      print(path)
      cv2.imwrite(path, frame)
      if count==100:
        text = 'Turn left your face 45 degree'
        print('Turn left your face 45 degree')
        time.sleep(3)
      if count==50:
        text ='Turn right your face 45 degree'
        print('Turn right your face 45 degree')
        time.sleep(3)
      count -= 1
      cv2.putText(frame, str(text), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
      cv2.imshow('Capture Face', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  cap.release()
  cv2.destroyAllWindows()

  announ = "Images Saved for Name : " + usr_name + " ID : " + usr_id
  header= ["ID", "Name"]
  row= [usr_id, usr_name]
  if(os.path.isfile("Student_Information"+os.sep+"StudentDetails.csv")):
     with open("Student_Information"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(j for j in row)
     csvFile.close()
  else:
     with open("Student_Information"+os.sep+"StudentDetails.csv", 'a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(i for i in header)
        writer.writerow(j for j in row)
     csvFile.close()
  print(announ)
  app.MainLoop()
if __name__ == '__main__':
    takeImages()