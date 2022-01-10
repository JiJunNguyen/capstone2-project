import os
import capture
import train_image
import detection


def title_bar():
    os.system('cls')

    # title of the program

    print("\t********************************************************************")
    print("\t----- Multi-Face Recognition System For Checking Attendance -----")
    print("\t********************************************************************")


# creating the simple user main interface

def mainMenu():
    title_bar()
    print()
    print(10 * "*", "Attendance System", 10 * "*")
    print("[1] Capture Faces")
    print("[2] Train Images")
    print("[3] Recognize & Attendance")
    print("[4] Send Email")
    print("[5] Finish Attendance System")

    while True:
        try:
            choice = int(input("Enter Choice: "))

            if choice == 1:
                CaptureFaces()
                break
            elif choice == 2:
                TrainImages()
                break
            elif choice == 3:
                DetectFaces()
                break
            elif choice == 4:
                SendMail()
                break
            elif choice == 5:
                print("Thank You For All")
                break
            else:
                print("Invalid Choice. Enter 1-5")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-5\n Try Again")
    exit


# --------------------------------------------------------------
# calling the take image function from capture.py file

def CaptureFaces():
    capture.takeImages()
    key = input("Enter any key to return main menu: ")
    mainMenu()


# -----------------------------------------------------------------
# calling the train images from train_image.py file

def TrainImages():
    train_image.align_mtcnn('your_face', 'face_align')
    train_image.train('face_align/', 'models/20180402-114759.pb', 'models/your_model.pkl')
    key = input("Enter any key to return main menu: ")
    mainMenu()


# --------------------------------------------------------------------
# calling the recognize_attendance from detection.py file

def DetectFaces():
    detection.recognize('models', 'models/your_model.pkl')
    key = input("Enter any key to return main menu: ")
    mainMenu()

# --------------------------------------------------------------------
def SendMail():
    os.system("py automail.py")
    key = input("Enter any key to return main menu: ")
    mainMenu()
# ---------------------------------------
mainMenu()
