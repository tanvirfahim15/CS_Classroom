from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify
from Service.OnlineClassroom import ClassroomHome as service

app = Blueprint('classroom_home', __name__)


@app.route("/classroom-courses-dashboard")
def show_course_dashboard():
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
        #print(data)
        service.join_class_info_update(data)
    return render_template('OnlineClassroom/classroom_with_courses/dashboard.html' ,**locals())


@app.route('/classroom-courses-create')
def show_create_classes():
    return render_template('OnlineClassroom/classroom_with_courses/create_classes.html', **locals())


@app.route('/classroom-courses-create/entry-data', methods=['POST', 'GET'])
def show_create_classes_entry_data():
    if request.method=='POST':
        data = request.form
        service.create_class_info_update(data)
    return render_template('OnlineClassroom/classroom_with_courses/dashboard.html' ,**locals())
