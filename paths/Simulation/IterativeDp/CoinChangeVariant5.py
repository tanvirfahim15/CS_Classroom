import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import CoinChangeVariant5 as ccv5

app = Blueprint('coin_change_variant5', __name__)


@app.route("/idp/coin-change-variant-5/entry", methods=['POST', 'GET'])
def coin_change_variant5_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant5_entry.html', **locals())


@app.route("/idp/coin-change-variant-5/entry_data", methods=['POST', 'GET'])
def coin_change_variant5_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'coin_array_variant5': data['coin_array_variant5'],'payment_variant5': data['payment_variant5']}
        posts = db.coin_change_variant5
        post_id = posts.insert_one(data).inserted_id
        print("herer ami")
        return redirect('/idp/coin-change-variant-5/' + str(post_id))
    return redirect('/idp/coin-change-variant-5/entry')


@app.route('/idp/coin-change-variant-5/<string:name>/')
def coin_change_variant5_simulation(name):
    data = db.coin_change_variant5.find_one({"_id": ObjectId(name)})
    coin_array1 = ast.literal_eval(data['coin_array_variant5'])
    coin_array2 = []
    coin_array2.append(0)
    for i in range(len(coin_array1)):
        coin_array2.append(int(coin_array1[i]))
    k = len(coin_array1)
    payment = data['payment_variant5']
    print(str(payment) + " yes here ")
    l_temp = ccv5.CoinChangeVariant5(int(payment), k , coin_array2)
    data = l_temp.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "coin_change_variant5"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant5_simulation.html', **locals())
