from flask import Blueprint
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from Service.OnlineClassroom import ClassroomFeed as service
app = Blueprint('classroom_feed', __name__)


@app.route("/news-feed")
def show_news_feed():
    data = service.show_news_feed()
    return render_template('OnlineClassroom/post_and_comment/feed.html', **locals())


@app.route("/entry_data" , methods=['POST', 'GET'])
def update_post():
    if request.method=="POST":
        data = request.form
        service.update_post(data)
    return redirect('/news-feed')


@app.route("/comment_entry/<id>" , methods=['POST', 'GET'])
def comment_entry(id):
    poststring , comments = service.comment_entry(id)
    return render_template('OnlineClassroom/post_and_comment/comment.html' ,poststring=poststring, comments=comments)


@app.route("/entry_comment/<id>" , methods=['POST', 'GET'])
def update_comment(id):
    if request.method=="POST":
        data = request.form
        service.update_comment(id ,data)
    return redirect('/comment_entry/'+str(id))
