from datetime import datetime
import string
from flask import render_template, request, redirect, session, Blueprint
from utility.database import db

app = Blueprint('auth', __name__)


@app.route("/auth/login/")
def login(data=None):
    if 'username' in session.keys():
        return redirect('/profile/'+session['username'])
    return render_template(
        'auth/login.html', **locals())


@app.route("/auth/logout")
def logout():
    if 'username' in session.keys():
        session.pop('username')
    return redirect('/')


@app.route("/auth/login-validation", methods=['POST', 'GET'])
def login_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        username = data['username']
        password = data['password']
        flag = True
        find = db.users.find_one({"username": str(username)})
        if find is None:
            flag = False
            data['username_msg'] = 'Username does not Exist'
        elif find['password'] != password:
            flag = False
            data['password_msg'] = 'Wrong password'
        if flag is False:
            return login(data)
        session['username'] = username
        return redirect('/profile/'+session['username'])


@app.route("/auth/register")
def register(data=None):
    if 'username' in session.keys():
        return redirect('/')
    return render_template(
        'auth/register.html', **locals())


@app.route("/auth/change-info")
def change_info(data=None):
    if 'username' not in session.keys():
        return redirect('/')
    if data is None:
        data = db.users.find_one({"username": session['username']})
        data.pop('_id')
    return render_template(
        'auth/change_info.html', **locals())


@app.route("/auth/change-info-validation", methods=['POST', 'GET'])
def change_info_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        password = data['password']
        c_password = data['c_password']
        email = data['email']
        birthday = data['birthday']
        institute = data['institute']
        country = data['country']
        occupation = data['occupation']
        flag = True

        if len(password) < 6:
            flag = False
            data['password_msg'] = 'Password length must be at least 6.'

        if password != c_password:
            flag = False
            data['c_password_msg'] = 'Password did not match.'

        find = db.users.find_one({"email": str(email)})
        if find is not None and find['username'] != session['username']:
            flag = False
            data['email_msg'] = 'Email belongs to another account'

        if '@' not in email:
            flag = False
            data['email_msg'] = 'Email format is not correct'
        elif '.' not in email.split('@')[1]:
            flag = False
            data['email_msg'] = 'Email format is not correct'

        date = datetime.strptime(birthday, '%Y-%m-%d')
        if date > datetime.today():
            flag = False
            data['birthday_msg'] = 'Invalid Birthday'

        if country == 'Choose...':
            flag = False
            data['country_msg'] = 'Choose one'

        if occupation == 'Choose...':
            flag = False
            data['occupation_msg'] = 'Choose one'

        for ch in institute:
            if ch not in string.ascii_letters and ch != '.' and ch != ' ':
                flag = False
                data['institute_msg'] = 'Institute can contain [a-z][A-z][.] only.'

        if flag is True:
            data.pop('c_password')
            data['username']=session['username']
            db.users.remove({'username': session['username']})
            db.users.insert_one(data)
            return redirect('/profile/'+session['username'])

        return change_info(data)


@app.route("/auth/register-validation", methods=['POST', 'GET'])
def register_validation():
    if request.method == 'POST':
        data = request.form.to_dict()
        username = data['username']
        password = data['password']
        c_password = data['c_password']
        email = data['email']
        birthday = data['birthday']
        gender = data['gender']
        institute = data['institute']
        country = data['country']
        occupation = data['occupation']
        flag = True

        if len(username) < 6:
            flag = False
            data['username_msg'] = 'Username must be atleast 6 characters.'

        find = db.users.find_one({"username": str(username)})
        if find is not None:
            flag = False
            data['username_msg'] = 'Username Exists'

        for ch in username:
            if ch not in string.ascii_letters and ch not in string.digits:
                flag = False
                data['username_msg'] = 'Username can contain [a-z][A-z][0-9] only.'

        if len(password) < 6:
            flag = False
            data['password_msg'] = 'Password length must be at least 6.'

        if password != c_password:
            flag = False
            data['c_password_msg'] = 'Password did not match.'

        find = db.users.find_one({"email": str(email)})
        if find is not None:
            flag = False
            data['email_msg'] = 'Email Exists'

        if '@' not in email:
            flag = False
            data['email_msg'] = 'Email format is not correct'
        elif '.' not in email.split('@')[1]:
            flag = False
            data['email_msg'] = 'Email format is not correct'

        date = datetime.strptime(birthday, '%Y-%m-%d')
        if date > datetime.today():
            flag = False
            data['birthday_msg'] = 'Invalid Birthday'

        if gender == 'Choose...':
            flag = False
            data['gender_msg'] = 'Choose one'

        if country == 'Choose...':
            flag = False
            data['country_msg'] = 'Choose one'

        if occupation == 'Choose...':
            flag = False
            data['occupation_msg'] = 'Choose one'

        for ch in institute:
            if ch not in string.ascii_letters and ch != '.' and ch != ' ':
                flag = False
                data['institute_msg'] = 'Institute can contain [a-z][A-z][.] only.'

        if 'terms' not in data.keys():
            flag = False
            data['terms_msg'] = 'You must agree to register'

        if flag is True:
            data.pop('c_password')
            data.pop('terms')
            posts = db.users
            posts.insert_one(data)
            return redirect('/auth/login')

        return register(data)

