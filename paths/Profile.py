from flask import render_template, request, redirect, session, Blueprint
from utility import Country
from utility.database import db


app = Blueprint('profile', __name__)


@app.route("/profile/<string:username>")
def profile(username):
    if 'username' not in session.keys():
        return redirect('/auth/login')
    if username != session['username']:
        return redirect('/')
    else:
        user_data = db.users.find_one({'username': session['username']})
        institute = user_data['institute']
        country = user_data['country']
        country = Country.country[country]
        posts = db.saved_simulation.find({'username': session['username']})
        data = []
        for post in posts:
            post.pop('_id')
            data.append(post)
        return render_template(
            'auth/profile.html', **locals())


@app.route("/profile/save_simulation", methods=['POST', 'GET'])
def save_simulation():
    if request.method == 'POST':
        data = request.form.to_dict()
        posts = db.saved_simulation
        posts.insert_one(data)
        return str('saved')


@app.route("/profile/remove_simulation", methods=['POST', 'GET'])
def remove_simulation():
    if request.method == 'POST':
        data = request.form.to_dict()
        posts = db.saved_simulation
        posts.remove(data)
        return str('removed')

# profile end
