from flask import request, render_template
from Database.database import db
import smtplib

class MyServer:
    def __init__(self):
        self.globalData = "hello"


    def function(self):
        print("Here1")
        return render_template("educational_management/admin_stu_add.html")

    def admin_stu_add(self,my_person):
        print("Here2x   ")
        # if not session.get('role') or session['role'] != 'admin':
        #     error = "You are not logged in or you are not an administrator"
        #     return render_template("educational_management/login.html", error=error)
        if request.method == 'POST':
            # cursor = get_db()
            # sno = request.form['sno']
            # sname = request.form['sname']
            # ssex = request.form['ssex']
            # sage = request.form['sage']
            # sdept = request.form['sdept']
            # sphone = request.form['sphone']
            # spassword = request.form['spassword']

            print("In adding student")

            # print(sname)
            info=my_person.getDescription()

            sno = info['Id']
            sname = info['Name']
            ssex = info['Gender']
            sage = info['Age']
            sdept = request.form['sdept']
            sphone = info['Phone']
            semail = info['Email']

            print(sno, sname, ssex, sage, sdept, sphone,semail)

            info['Department']=request.form['sdept']
            enroll_stu = db.xenrolled_student
            enroll_stu.insert_one(info)


            # sending mail
            subject = "Enrollment in Online Classroom"
            msg = "Hello "+sname+",\n  You have been enrolled in CS Online Classroom as a "+info['Person']
            send_email(subject, msg,semail)



        return render_template('manage_classroom/admin_stu_add.html')



def send_email(subject, msg, semail):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        EMAIL_ADDRESS= "online14classroom@gmail.com"
        PASSWORD="online.14.classroom"
        server.login(EMAIL_ADDRESS, PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)

        receiver=semail
        server.sendmail(EMAIL_ADDRESS, receiver,message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


    return