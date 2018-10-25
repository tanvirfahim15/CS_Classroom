import  ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import SCS as scs

app = Blueprint('scs', __name__)

@app.route("/idp/shortest-common-supersequence/entry", methods=['POST', 'GET'])
def shortest_common_supersequence_entry():
    return render_template(
        'simulation/scs_iterative_dp/scs_iterative_dp_entry.html', **locals())


@app.route("/idp/shortest-common-supersequence/entry_data", methods=['POST', 'GET'])
def shortest_common_supersequence_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'string1' : data['string1'],'string2' : data['string2']}
        posts = db.shortest_common_supersequence
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/shortest-common-supersequence/' + str(post_id))
    return redirect('/idp/shortest-common-supersequence/entry')


@app.route('/idp/shortest-common-supersequence/<string:name>/')
def shortest_common_supersequence_simulation(name):
    data = db.shortest_common_supersequence.find_one({"_id": ObjectId(name)})
    l_temp = scs.SCS(data['string1'], data['string2'])
    data = l_temp.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "lcs"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/scs_iterative_dp/scs_iterative_dp_simulation.html', **locals())