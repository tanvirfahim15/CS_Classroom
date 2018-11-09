from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify,flash

from Database.database import db
from Service.OnlineClassroom import ClassroomHome as service
from classes.ClassManagement.ObserverPattern.AdminObserver import AdminObserver
from classes.ClassManagement.ObserverPattern.EnrollmentData import EnrollmentData

app = Blueprint('classroom_home', __name__)


@app.route("/classroom-courses-dashboard")
def show_course_dashboard():
    if "username" not in session.keys():
        return redirect("/auth/login/")


    # start
    enrollstu = db.xenrolled_student.find(
        {
            "Name": session['username']
        }
    )


    # teacher not implemented yet
    enrolltea = db.xenrolled_teacher.find(
        {
            "tName": session['username']
        }
    )

    flag = 0

    for x in enrollstu:
        print(x['Name'])
        if (session['username'] == x['Name']):
            flag = 1

    for x in enrolltea:
        print(x['Name'])
        if (session['username'] == x['tName']):
            flag = 2


    if (flag == 0):
        return render_template('manage_classroom/access_denied.html')


    # end
    return render_template('OnlineClassroom/classroom_with_courses/dashboard.html', **locals())


@app.route("/classroom-courses-enrolled")
def show_enrolled_classes():
    courses = service.enrolled_class_info_show()
    return render_template('OnlineClassroom/classroom_with_courses/enrolled_classes.html', **locals())


@app.route('/classroom-courses-join')
def show_join_classes():
    return render_template('OnlineClassroom/classroom_with_courses/join_classes.html' ,**locals())


@app.route('/classroom-courses-join/entry-data', methods=['POST', 'GET'])
def show_join_classes_entry_data():
    if request.method=='POST':
        data = request.form
        data['course_id'].strip()
        if len(data['course_id']) != 24:
            flash("Invalid Class Code!")
            return redirect('/classroom-courses-join')
        get_error = service.join_class_info_update(data)
        if get_error == -1:
            # print("flashing")
            flash("Invalid Class Code!")
            return redirect('/classroom-courses-join')
        #print(data)
        # service.join_class_info_update(data)
        if get_error == 1:
            flash('Successfully joined the class.')
        else:
            flash('You are already enrolled into the class.')
    return render_template('OnlineClassroom/classroom_with_courses/dashboard.html' ,**locals())


@app.route('/classroom-courses-create')
def show_create_classes():
    return render_template('OnlineClassroom/classroom_with_courses/create_classes.html', **locals())


@app.route('/classroom-courses-create/entry-data', methods=['POST', 'GET'])
def show_create_classes_entry_data():
    if request.method=='POST':
        data = request.form



        #print(data['course_name'])
        #print(data['course_code'])


        # start
        createClassData = data
        enrollData = EnrollmentData()

        adminObserver = AdminObserver()
        enrollData.registerObserver(adminObserver)
        enrollData.putTeacherRequest(createClassData)
        enrollData.removeObserver(adminObserver)

        #end

        # service.create_class_info_update(data)
        flash('Successfully created the '+str(data['course_name'])+' class.')
    return render_template('OnlineClassroom/classroom_with_courses/dashboard.html' ,**locals())


@app.route('/leave_class/<course_id>')
def leave_class(course_id):
    service.leave_class_info_update(course_id)
    return redirect('/classroom-courses-dashboard')


@app.route('/course_details/<course_id>')
def course_details(course_id):
    # print(course_id)
    users = service.course_details(course_id)
    return render_template('OnlineClassroom/classroom_with_courses/course_details.html', **locals())