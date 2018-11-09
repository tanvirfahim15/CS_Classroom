from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify,flash
from Service.OnlineClassroom import ClassroomFeed as service
from pattern.AdapterPattern.addclasstopost import addclasstopost
from pattern.AdapterPattern.assignmenttopost import assignmenttopost

app = Blueprint('classroom_feed', __name__)


@app.route("/news-feed/<course_id>")
def show_news_feed(course_id):
    enrolled_flag = service.check_is_enrolled(course_id)
    if enrolled_flag == -1:
        flash('You are not enrolled. Join the class please.')
        return redirect('/classroom-courses-dashboard')
    course_info, data, users, notifications = service.show_news_feed(course_id)
    classmate_count = len(course_info['enrolled'])
    return render_template('OnlineClassroom/post_and_comment/feed.html', **locals())


@app.route("/entry_data/<course_id>" , methods=['POST', 'GET'])
def update_post(course_id):
    if request.method=="POST":
        data = request.form
        # print(data)
        if len(data['message']) != 0:
            service.update_post(data , course_id)
        else:
            flash("Post is empty!! Write something..")
    return redirect('/news-feed/'+str(course_id))


@app.route("/comment_entry/<id>/<course_id>" , methods=['POST', 'GET'])
def comment_entry(id, course_id):
    poststring , comments , course_info , notifications= service.comment_entry(id, course_id)
    classmate_count = len(course_info['enrolled'])
    return render_template('OnlineClassroom/post_and_comment/comment.html' ,**locals())


@app.route("/entry_comment/<id>/<course_id>/<author>" , methods=['POST', 'GET'])
def update_comment(id, course_id,author):
    print(id+" "+course_id+" "+author)
    if request.method=="POST":
        data = request.form
        service.update_comment(id ,course_id,data,author)

    return redirect('/comment_entry/'+str(id)+'/'+str(course_id))


@app.route("/assignment/<course_id>")
def assingmnet(course_id):
    return render_template('OnlineClassroom/post_and_comment/giveassignment.html', **locals())


@app.route('/add_assignment/<course_id>')
def add_assignment(course_id):
    time = request.args.get('time', 0, type=str)
    date = request.args.get('date', 0, type=str)
    details= request.args.get('details', 0, type=str)
    # print(time)
    # print(date)
    # print(details)
    assignmenttopost(time,date,details,session['username'],course_id)
    return jsonify(result="assignment added")


@app.route('/class/<course_id>')
def class_add(course_id):
    return render_template('OnlineClassroom/post_and_comment/addclass.html', **locals() )


@app.route('/add_class/<course_id>')
def add_class(course_id):
    starttime = request.args.get('starttime', 0, type=str)
    endtime = request.args.get('endtime', 0, type=str)
    details= request.args.get('details', 0, type=str)
    # print(starttime)
    # print(endtime)
    # print(details)
    addclasstopost(starttime,endtime,details,session['username'],course_id)
    return jsonify(result="new class time has been announced")


@app.route('/give_mcq')
def give_mcq():
    print("sdfasfsafsfa")
    return render_template('OnlineClassroom/post_and_comment/give_mcq.html',**locals())


@app.route('/create_mcq')
def create_mcq():
    qno=1
    return render_template('OnlineClassroom/post_and_comment/create_mcq.html',**locals())


@app.route('/create_question/<qno>' , methods=['POST', 'GET'])
def create_question(qno):
    if request.method=="POST":
        data = request.form
        print(data)
    qno=int(qno)
    qno+=1
    print(qno)
    return render_template('OnlineClassroom/post_and_comment/create_mcq.html',**locals())


@app.route('/create_last_question/<qno>' , methods=['POST', 'GET'])
def create_last_question(qno):
    if request.method=="POST":
        data = request.form
        print(data)
    qno=int(qno)
    qno+=1
    print(qno)
    return render_template('OnlineClassroom/post_and_comment/successfully_quiz_created.html',**locals())