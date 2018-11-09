from bson import ObjectId
from flask import session
from Database.database import db
from pattern.SendNotifications import NotificationSender


def create_class_info_update(data):
    course_info = {'course_name':data['course_name'], 'course_code':data['course_code'], 'enrolled':[]}
    course_info['enrolled'].append(session['username'])

    print(course_info)
    course_id = db.courses.insert_one(course_info).inserted_id
    user = db.course_users.find_one({'username':session['username']})
    if user == None:
        user = {'username':session['username'], 'course_id':[]}
        db.course_users.insert_one(user)
        user = db.course_users.find_one({'username':session['username']})
    if course_id not in user['course_id']:
        user['course_id'].append(course_id)
    db.course_users.replace_one({'username': session['username']}, user)
    return


def space_check(s):
    for i in range(0, 24):
        if s[i]==' ':
            return -1
    return 1


def join_class_info_update(data):
    user = db.course_users.find_one({'username': session['username']})
    if user==None:
        user = {'username':session['username'], 'course_id':[]}
        db.course_users.insert_one(user)
        user = db.course_users.find_one({'username': session['username']})

    courses = user['course_id']
    if data['course_id'] not in courses:
        user['course_id'].append(data['course_id'])
        # db.courses.replace_one({'_id': ObjectId(self.course_id)}, course)
        db.course_users.replace_one({'username': session['username']} , user)

    course_id = data['course_id']
    if len(course_id) != 24:
        return -1
    got_ret = space_check(str(course_id))
    if got_ret == -1:
        return -1
    course = db.courses.find_one({'_id': ObjectId(course_id)})
    if course == None:
        return -1
    users = course['enrolled']
    if session['username'] not in users:
        NotificationSender.Sender(course_id, "").register_observer(session['username'])
    else:
        return 2

    return 1


def enrolled_class_info_show():
    courses = db.course_users.find_one({'username':session['username']})
    # print(courses)
    if courses is None:
        course_list = []
        return course_list
    courses = courses['course_id']
    course_list = []
    for cid in courses:
        course_datails = db.courses.find_one({"_id": ObjectId(cid)})
        needed_count = len(course_datails['enrolled'])
        needed_details = {'_id': course_datails['_id'],'course_code': course_datails['course_code'], 'course_name':course_datails['course_name'], 'enrolled:':course_datails['enrolled'],'count': needed_count }
        course_list.append(needed_details)
        # print(course_datails)
    # print(course_list)
    return course_list


def leave_class_info_update(course_id):
    course = db.courses.find_one({'_id':ObjectId(course_id)})
    if course is None:
        return
    NotificationSender.Sender(course_id, "").remove_observer(session['username'])
    user_info = db.course_users.find_one({'username':session['username']})
    if user_info is None:
        # print(user_info)
        # print(session['username'])
        return
    # print(user_info['course_id'])
    if course_id in user_info['course_id']:
        user_info['course_id'].remove(course_id)
    if ObjectId(course_id) in user_info['course_id']:
        user_info['course_id'].remove(ObjectId(course_id))
    # print(user_info['course_id'])
    db.course_users.replace_one({'username':session['username']}, user_info)
    return


def course_details(course_id):
    course = db.courses.find_one({'_id':ObjectId(course_id)})
    if course is None:
        return None
    users=[]
    for user in course['enrolled']:
        tmpUser = db.course_users.find_one({'username':user})
        if tmpUser is not None:
            tmpCourseList = []
            for tmpCourse in tmpUser['course_id']:
                tmpCourse = db.courses.find_one({'_id':ObjectId(tmpCourse)})
                tmpCourse = tmpCourse['course_name']
                tmpCourseList.append(tmpCourse)
            users.append({'username':tmpUser['username'],'course_list':tmpCourseList})
    # print(users)
    return users
