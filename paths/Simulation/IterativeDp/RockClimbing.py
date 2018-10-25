import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import RockClimbing as rc

app = Blueprint('rock_climbing', __name__)

@app.route("/idp/rock-climbing/entry", methods=['POST', 'GET'])
def rock_climbing_entry():
    return render_template(
        'simulation/rockclimbing_iterative_dp/rockclimbing_iterative_dp_entry.html', **locals())


@app.route("/idp/rock-climbing/entry_data", methods=['POST', 'GET'])
def rock_climbing_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'string1' : data['string1'],'string2' : data['string2']}
        posts = db.rock_climbing
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/rock-climbing/' + str(post_id))
    return redirect('/idp/rock-climbing/entry')


@app.route('/idp/rock-climbing/<string:name>/')
def rock_climbing_simulation(name):
    data = db.rock_climbing.find_one({"_id": ObjectId(name)})
    l_temp = rc.RockClimbing(data['string1'], data['string2'])
    data = l_temp.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lcs"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/rockclimbing_iterative_dp/rockclimbing_iterative_dp_simulation.html', **locals())