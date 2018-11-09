from bson import ObjectId
from flask import session
from Database.database import db
from pattern.SendNotifications import NotificationSender
from pattern.SendCommentsNotification import CommentsNotificationSender
from classes.OnlineClassroom.createPost import post
from pattern.CreatePostUsingBuilderPattern.Post import Post


def check_is_enrolled(course_id):
    course = db.courses.find_one({'_id':ObjectId(course_id)})
    if course is None:
        return -1
    if session['username'] in course['enrolled']:
        return 1
    return -1


def show_news_feed(course_id):
    pymongo_cursor = db.classroom_newsfeed.find({'course_id':course_id})
    all_data = list(pymongo_cursor)
    data = all_data
    # print(data)
    data.reverse()
    # print(data)
    course = db.courses.find_one({'_id':ObjectId(course_id)})
    users = course['enrolled']
    if session['username'] not in users:
        NotificationSender.Sender(course_id, "").register_observer(session['username'])
    notifications = db.notifications.find_one({'username': session['username']})
    if notifications == None:
        notifications = []
    else:
        notifications = notifications['notifications']
    notifications.reverse()
    return course, data, users, notifications


def update_post(data , course_id):
    # postdetails=post(data['message'],data['files'],session['username'], course_id)
    postdetails=Post.PostBuilder(course_id)\
        .with_author(session['username'])\
        .with_text(data['message'])\
        .with_links(data['links'])\
        .build()
    post_id=save_to_database1(postdetails)
    # print(session['username'])
    course = db.courses.find_one({'_id': ObjectId(course_id)})
    course_name = course['course_name']
    notification = {"course_id":course_id, "course_name":course_name,"notification_type": "post", "username": session['username']}
    NotificationSender.Sender(course_id, notification).notify_observer()
    return


def comment_entry(id, course_id):
    course_info = db.courses.find_one({'_id': ObjectId(course_id)})
    notifications = db.notifications.find_one({'username': session['username']})
    if notifications == None:
        notifications = []
    else:
        notifications = notifications['notifications']
    poststring=db.classroom_newsfeed.find_one({'_id': ObjectId(id)});
    pymongo_cursor = db.comments.find( { "postid" : id} )
    all_comments = list(pymongo_cursor)
    comments= all_comments
    notifications.reverse()
    return poststring, comments, course_info, notifications


def update_comment(id ,course_id, data,author):
    data = {"posttext": data['message'],"postid":id ,  "authors": session['username']}
    posts = db.comments
    post_id = posts.insert_one(data).inserted_id
    course = db.courses.find_one({'_id': ObjectId(course_id)})
    course_name = course['course_name']
    notification = {"course_id": course_id, "course_name": course_name, "notification_type": "comment",
                    "username": session['username'] ,"author":author}
    CommentsNotificationSender.CommentSender(course_id, notification).notify_observer()
    return


def save_to_database1(postdetails):
    data = {"posttext": postdetails.get_post_text(),
            "authors": postdetails.get_author(), "course_id": postdetails.get_course_id(),"links":postdetails.get_links()}
    posts = db.classroom_newsfeed
    return posts.insert_one(data).inserted_id


def save_to_database(postdetails):
    data = {"posttext": postdetails.getposttext(), "postfile": postdetails.getpostfile(),
            "authors": postdetails.getauthor(), "course_id": postdetails.get_course_id()}
    posts = db.classroom_newsfeed
    return posts.insert_one(data).inserted_id


def save_quiz_to_databse(quiz , course_id):
    # print(quiz.add_more_question())
    quizList = quiz.add_more_question()
    data ={'course_id': course_id , 'quiz_name': quiz.get_quiz_name(), 'questions':[]}

    for question in quizList:
        tmpData = {'question':question.getQuestion(), 'option1':question.getOption1() , 'option2':question.getOption2() ,'option3':question.getOption3(), 'option4':question.getOption4(),'correct_answer':question.getCorrectAnswer()}
        # print(question.getQuestion())
        # print(question.getOption1())
        # print(question.getOption2())
        # print(question.getOption3())
        # print(question.getOption4())
        # print(question.getCorrectAnswer())
        data['questions'].append(tmpData)

    db.quiz.insert_one(data)

    return



def get_quiz_lists(course_id):
    pymongo_cursor = db.quiz.find({'course_id': course_id})
    all_data = list(pymongo_cursor)
    data = all_data
    quiz_lists = []
    for dt in data:
        tmpDT ={'quiz_name':dt['quiz_name'] , 'quiz_id':dt['_id']}
        quiz_lists.append(tmpDT)
    print(quiz_lists)
    return quiz_lists


def get_quiz_data(quiz_id):
    curse = db.quiz.find_one({'_id': ObjectId(quiz_id)})
    data=curse['questions']
    print(data)
    return curse

