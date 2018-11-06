import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = 'csclassroom89@gmail.com'
password = 'csclassroomcsedu'


def SendMessage(to, subject, msgHtml, msgPlain):
    send_email(username, password, to, subject, msgHtml, msgPlain)


def send_email(user, pwd, recipient, subject, html, text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = recipient
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(user, recipient, msg.as_string())
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")