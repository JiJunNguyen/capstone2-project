import yagmail
import smtplib
import os
import datetime
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# making tkinter window
win = Tk()
win.iconbitmap('icons\send.ico')
win.title("Send Email")
win.geometry('500x530+10+10')

# variable for Login box
Email = StringVar()
Password = StringVar()

# Login layout
def login():
    global email
    frame = Frame(win, width=500, height=530,  bg='white')

    acc_img = ImageTk.PhotoImage(Image.open("icons/account.png"))
    acc_icon = Label(frame, image=acc_img, bg='white')
    acc_icon.image = acc_img

    title_lb = LabelFrame(frame, text='Sign in to continue', font=("Helvetica", 18, "bold"), fg='#666A6C', bg='white',labelanchor = 'n')

    email_lb = LabelFrame(frame, text='Email', font=("Helvetica", 12, "bold"), fg='#4C4A49', bg='white')
    email = ttk.Entry(email_lb, textvariable = Email,  width=35)

    pass_lb = LabelFrame(frame, text='Password', font=("Helvetica", 12, "bold"), fg='#4C4A49', bg='white')
    password = ttk.Entry(pass_lb, textvariable=Password, width=35, show="*")

    button_login = ttk.Button(frame, text='Login',command=acc_verify)


    acc_icon.place(x=173, y=20)
    title_lb.place(x=75, y=170, width=350, height=275)
    email_lb.place(x=125, y=230, width=250, height=55)
    email.pack()
    pass_lb.place(x=125, y=305, width=250, height=55)
    password.pack()
    button_login.place(x=300, y=390)

    frame.place(x=0, y=0)

def acc_verify():
    global server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    try:
        server.login(Email.get(), Password.get())
        mail_compose()
    except Exception:
        messagebox.showerror(title='Sign in Error!', message='Please check your Email and Password')

# Mail compose layout
def mail_compose():
    frame = Frame(win, width=500,height=530,  bg='white')
    def mail():
        send_to_email = recei_tx.get()
        #date = datetime.date.today().strftime("%d-%m-%Y")
        date_sub = date_tx.get()
        sub_name = sub_tx.get()
        class_period = period_tx.get()
        subject = '[Report]'+'['+str(sub_name)+']'+'['+str(date_sub)+']'
        message = 'Here is the attendance report for '+ str(sub_name)+' on '+str(date_sub)
        file_location = 'C:\\Users\\ACER.LAPTOP-PI98O0EL\\PycharmProjects\\capstone2_project\\venv\\Attendance\\Student_Attendance\\'+str(sub_name)+'_'+str(date_sub)+'_'+str(class_period)+'.csv'

        msg = MIMEMultipart()
        msg['From'] = str(Email.get())
        msg['To'] = send_to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Setup the attachment
        filename = os.path.basename(file_location)
        attachment = open(file_location, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        # Attach the attachment to the MIMEMultipart object
        msg.attach(part)

        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(Email.get(), Password.get())  # login with mail_id and password
        text = msg.as_string()
        session.sendmail(Email.get(), send_to_email, text)
        session.quit()

        messagebox.showinfo(title='Announcement', message='Mail has been sent')
    # Create the function to delete all info for sending new mess
    def delete():
        recei_tx.delete(0, END)
        sub_tx.delete(0, END)
        date_tx.delete(0, END)
        period_tx.delete(0, END)


    title_com = Label(frame, text="Compose", font=("Helvetica", 25,'bold'), bg='white', fg="#F85858")
    title_com.place(x=30, y=25)

    recei = LabelFrame(frame, text="To Email",bg = 'white')
    subject = LabelFrame(frame, text="Subject Title",bg = 'white')
    date = LabelFrame(frame, text="Date (DD-MM-YYYY)",bg = 'white')
    period = LabelFrame(frame, text="Class Period", bg='white')

    button_send = ttk.Button(frame, text="Send", command=mail)
    button_delete = ttk.Button(frame, text="Clear", command=delete)

    recei_tx = ttk.Entry(recei, width=60)
    sub_tx = ttk.Entry(subject, width=60)
    date_tx = ttk.Entry(date, width=60)
    period_tx = ttk.Entry(period, width=60)


    recei.place(x=30, y=100, height=45, width=400)
    subject.place(x=30, y=180, height=45, width=400)
    date.place(x=30, y=260, height=45, width=400)
    period.place(x=30, y=340, height=45, width=400)

    button_send.place(x=30, y=455)
    button_delete.place(x=130, y=455)

    recei_tx.pack()
    sub_tx.pack()
    date_tx.pack()
    period_tx.pack()

    frame.place(x=0, y=0)

# Verify mail after entering email and pass
# It will show error when login fail


if __name__ == '__main__':
    login()
    win.mainloop()