from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify
from Service.OnlineClassroom import ClassroomHome as service
from classes.ClassManagement.mailToppings import mailToppings
from classes.ClassManagement.BasicStudent import BasicStudent
from classes.ClassManagement.addStudent import MyServer, send_email
from classes.ClassManagement.ageToppings import ageToppings
from classes.ClassManagement.genderTopping import genderToppings
from classes.ClassManagement.mediatorpattern.AdminUpdate import AdminUpdate
from classes.ClassManagement.mediatorpattern.Mediator import Mediator
from classes.ClassManagement.mediatorpattern.getMediatorInstance import getMediatorInstance
from classes.ClassManagement.nameToppings import nameToppings

from classes.ClassManagement.phonenumberToppings import phonenumberToppings
from classes.ClassManagement.studentidtoppings import studentidtoppings

from Database.database import db
from flask_mail import Message, Mail

app = Blueprint('manage_classroom', __name__)


@app.route("/manage_classroom")
def show_course_dashboard():

    print("shohan")
    # if "username" not in session.keys():
    #     return redirect("/auth/login/")
    # return render_template('manage_classroom/admin_page.html', **locals())
    return render_template('manage_classroom/enter_classroom.html', **locals())








@app.route("/access_control", methods=['POST', 'GET'])
def access_control():


    if request.method == 'POST':
        print("delete")
        role = request.form.get('role')
        passw= request.form.get('password')

        print(role,passw)

        if(role!='admin' and passw!='admin'):
            return render_template('manage_classroom/enter_classroom.html', **locals())


    print("shohan")
    # if "username" not in session.keys():
    #     return redirect("/auth/login/")
    # return render_template('manage_classroom/admin_page.html', **locals())
    return render_template('manage_classroom/admin_page.html', **locals())





@app.route("/admin_navi")
def admin_navi():

    print("shohan")
    # if "username" not in session.keys():
    #     return redirect("/auth/login/")
    # return render_template('OnlineClassroom/classroom_with_courses/dashboard.html', **locals())
    return render_template('manage_classroom/admin_navi.html')



@app.route("/admin_dummy")
def admin_dummy():



    # if(flag==0):
         # return render_template('manage_classroom/admin_page.html', message="You dont have access")


    # if "username" not in session.keys():
    #     return redirect("/auth/login/")
    # return render_template('OnlineClassroom/classroom_with_courses/dashboard.html', **locals())
    return "Happy"

#
# @app.route("/admin_stu_add")
# def admin_stu_add():
#
#     print("shohan")
#     # if "username" not in session.keys():
#     #     return redirect("/auth/login/")
#     # return render_template('OnlineClassroom/classroom_with_courses/dashboard.html', **locals())
#     return render_template('manage_classroom/admin_stu_add.html')
#

my_server = MyServer()
my_person= BasicStudent()

@app.route('/admin_stu_add', methods=['POST', 'GET'])  #, methods=['POST', 'GET']
def admin_stu_add():
    global my_person
    return my_server.admin_stu_add(my_person)



@app.route('/receivedata', methods=['POST'])
def receive_data():
    global my_person
    print("in receiving")

    if(request.form.get('sno')!=None):
        my_person= studentidtoppings(request.form.get('sno'),my_person)
        # print(request.form.get('sno'))

    if (request.form.get('sname') != None):
        my_person = nameToppings(request.form.get('sname'), my_person)
        # print(request.form.get('sname'))

    if (request.form.get('ssex') != None):
        my_person = genderToppings(request.form.get('ssex'), my_person)

    if (request.form.get('sage') != None):
        my_person = ageToppings(request.form.get('sage'), my_person)

    if (request.form.get('sphone') != None):
        print("receiving phone")
        my_person = phonenumberToppings(request.form.get('sphone'), my_person)

    if (request.form.get('semail') != None):
        print("receiving mail")
        my_person = mailToppings(request.form.get('semail'), my_person)


    print(my_person.getDescription())

    # print(request.form.get('ssex'))
    # print(request.form.get('sage'))
    # print(request.form.get('sphone'))
    # print(request.form.get('spassword'))



    return "shohan"



@app.route('/admin_stu_list', methods=['POST', 'GET'])
def admin_stu_list():
    # if not session.get('role') or session['role'] != 'admin':
    #     error = "You are not logged in or you are not an administrator"
    #     return render_template("educational_management/login.html", error=error)



    if request.method == 'POST':
        print("delete")
        deleteId=request.form.get('Id')
        db.xenrolled_student.remove(
            {
                "Id":deleteId
            }
        )

    data = []
    for cou in db.xenrolled_student.find():
        info = []
        info.append(cou['Id'])
        info.append(cou['Name'])
        info.append(cou['Department'])
        info.append(cou['Phone'])
        print(info)
        data.append(info)

    # print(student_result_set)
    # return render_template('student_enter_course.html', student_data=data)

    return render_template('manage_classroom/admin_stu_list.html', student_data=data)






@app.route('/admin_tea_add', methods=['POST', 'GET'])
def admin_tea_add():
    # if not session.get('role') or session['role'] != 'admin':
    #     error = "You are not logged in or you are not an administrator"
    #     return render_template("educational_management/login.html", error=error)
    if request.method == 'POST':
        info={}
        info['tId'] = request.form['tno']
        info['tName'] = request.form['tname']
        info['tPhone'] = request.form['tphone']
        info['tEmail'] = request.form['temail']

        enroll_tea = db.xenrolled_teacher
        # enroll_tea.insert_one(info)

        # Implementing mediator pattern
        mediator = getMediatorInstance()
        adminUpdate = mediator.adminUpdate
        adminUpdate.requestUpdate(enroll_tea, info)

        enroll_tea
        subject = "Enrollment in Online Classroom"
        msg = "Hello " + info['tName'] + ",\n  You have been enrolled in CS Online Classroom as a teacher"
        send_email(subject, msg, info['tEmail'])



    return render_template('manage_classroom/admin_tea_add.html')

@app.route('/admin_tea_list', methods=['POST', 'GET'])
def admin_tea_list():
    # if not session.get('role') or session['role'] != 'admin':
    #     error = "You are not logged in or you are not an administrator"
    #     return render_template("educational_management/login.html", error=error)



    if request.method == 'POST':
        print("delete tech")
        deleteId=request.form.get('Id')

        print(deleteId)
        db.xenrolled_teacher.remove(
            {
                "tId":deleteId
            }
        )

    data = []
    for cou in db.xenrolled_teacher.find():
        info = []
        info.append(cou['tId'])
        info.append(cou['tName'])
        info.append(cou['tPhone'])
        info.append(cou['tEmail'])
        print(info)
        data.append(info)

    # print(student_result_set)
    # return render_template('student_enter_course.html', student_data=data)

    return render_template('manage_classroom/admin_tea_list.html', teacher_data=data)