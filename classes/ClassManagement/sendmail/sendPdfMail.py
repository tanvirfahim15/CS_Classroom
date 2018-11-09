import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email
import email.mime.application

def sendPdfMail(fo,receiver): # need update
    receiver = list(set(receiver))

    html = """
    Dear,\n 
    This is an important notice from OnlineClassroom where you are subscribe.\n
    Best Regards."""

    # Creating message.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Notice from OnlineClassroom"
    msg['From'] = "online14classroom@gmail.com"
    msg['To'] = "musfuq14shohan@gmail.com"

    # The MIME types for text/html
    HTML_Contents = MIMEText(html, 'html')

    # Adding pptx file attachment
    # filename = '/home/musfiq/PycharmProjects/CS_Classroom_Updated/classes/ClassManagement/sendmail/mypdf.pdf'
    # fo = open(filename, 'rb')
    # attach = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")

    attach = email.mime.application.MIMEApplication(fo.read(), _subtype="pdf")
    fo.close()
    # return

    # attach.add_header('Content-Disposition', 'attachment', filename=filename)
    attach.add_header('Content-Disposition', 'attachment', filename=fo.filename)

    # Attachment and HTML to body message.
    msg.attach(attach)
    msg.attach(HTML_Contents)

    # Your SMTP server information
    s_information = smtplib.SMTP('smtp.gmail.com:587')
    # You can also use SSL
    # smtplib.SMTP_SSL([host[, port[, local_hostname[, keyfile[, certfile[, timeout]]]]]])
    # s_information.connect()
    s_information.ehlo()
    s_information.starttls()

    EMAIL_ADDRESS = "online14classroom@gmail.com"
    PASSWORD = "online.14.classroom"
    s_information.login(EMAIL_ADDRESS, PASSWORD)
    # s_information.sendmail(msg['From'], msg['To'], msg.as_string())


    for rec in receiver:
        print("sending to "+rec)
        s_information.sendmail(msg['From'], rec , msg.as_string())

    s_information.quit()
