import string
import random
import smtplib
from email.mime.text import MIMEText


def new_pass():
    temp_pass = ''
    chars = string.ascii_letters + string.digits
    pass_range = random.sample(list(chars), 44)
    for char in pass_range:
        temp_pass += char
    return temp_pass


def email_func(new_pass, email):
        sendTo = email
        msg = MIMEText('http://localhost:8080/enter_pass/' + new_pass)
        msg['Subject'] = 'Swindle - Account Update Notification'
        msg['From'] = 'noreply@dropthetranny.com'
        msg['To'] = sendTo
        #smtpObj = smtplib.SMTP('smtp.webfaction.com', 587)  #edit this line to send email from your webhost
        #smtpObj.login("username", "password")  #edit this line with your webhost username and password
        smtpObj.send_message(msg)
