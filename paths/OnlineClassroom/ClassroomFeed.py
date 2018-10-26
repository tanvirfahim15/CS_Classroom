from flask import Blueprint
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session,jsonify
from Service.OnlineClassroom import ClassroomFeed as service
app = Blueprint('classroom_feed', __name__)


@app.route("/news-feed")
def show_news_feed():
    course_id ='5bd316f051b1980fab57b706'
    data, users, notifications = service.show_news_feed(course_id)
    #print(notifications)
    return render_template('OnlineClassroom/post_and_comment/feed.html', **locals())


@app.route("/entry_data" , methods=['POST', 'GET'])
def update_post():
    course_id = '5bd316f051b1980fab57b706'
    if request.method=="POST":
        data = request.form
        service.update_post(data , course_id)
    return redirect('/news-feed')


@app.route("/comment_entry/<id>" , methods=['POST', 'GET'])
def comment_entry(id):
    poststring , comments = service.comment_entry(id)
    return render_template('OnlineClassroom/post_and_comment/comment.html' ,**locals())


@app.route("/entry_comment/<id>" , methods=['POST', 'GET'])
def update_comment(id):
    if request.method=="POST":
        data = request.form
        service.update_comment(id ,data)
    return redirect('/comment_entry/'+str(id))
@app.route("/assignment")
def assingmnet():
    return render_template('OnlineClassroom/post_and_comment/giveassignment.html')
@app.route('/add_assignment')
def add_numbers():
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=str)
    c = request.args.get('c', 0, type=str)
    print(a)
    print(b)
    print(c)
    return jsonify(result="assignment added")