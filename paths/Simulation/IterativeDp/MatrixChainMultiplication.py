import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import MatrixChainMultiplication as mcm

app = Blueprint('matrix_chain_multiplication', __name__)


@app.route("/idp/matrix-chain-multiplication/entry", methods=['POST', 'GET'])
def matrix_chain_multiplication_entry():
    return render_template(
        'simulation/mcm_iterative_dp/mcm_iterative_dp_entry.html', **locals())


@app.route("/idp/matrix-chain-multiplication/entry_data", methods=['POST', 'GET'])
def matrix_chain_multiplication_data_entry():
    if request.method == 'POST':
        data = request.form
        data = {'dimension_array' : data['dimension_array']}
        posts = db.matrix_chain_multiplication
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/matrix-chain-multiplication/' + str(post_id))
    return redirect('/idp/matrix-chain-multiplication/entry')


@app.route('/idp/matrix-chain-multiplication/<string:name>/')
def matrix_chain_multiplication_simulation(name):
    data = db.matrix_chain_multiplication.find_one({"_id": ObjectId(name)})
    dimensions = ast.literal_eval(data['dimension_array'])

    k = len(dimensions)

    l_temp = mcm.MatrixChainMultiplication(k, dimensions)
    data = l_temp.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "matrix_chain_multiplication"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/mcm_iterative_dp/mcm_iterative_dp_simulation.html', **locals())