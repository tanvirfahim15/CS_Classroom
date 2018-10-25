import ast
from bson import ObjectId
from flask import render_template, request, redirect, session, Blueprint
from Database.database import db
from classes.Simulation.IterativeDp import CoinChangeVariant2 as ccv2

app = Blueprint('coin_change_variant2', __name__)

@app.route("/idp/coin-change-variant-2/entry", methods=['POST', 'GET'])
def coin_change_variant2_entry():
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant2_entry.html', **locals())


@app.route("/idp/coin-change-variant-2/entry_data", methods=['POST', 'GET'])
def coin_change_variant2_entry_data():
    if request.method == 'POST':
        data = request.form
        data = {'coin_array_variant2' : data['coin_array_variant2'],'payment_variant2' : data['payment_variant2']}
        posts = db.coin_change_variant2
        post_id = posts.insert_one(data).inserted_id
        return redirect('/idp/coin-change-variant-2/' + str(post_id))
    return redirect('/idp/coin-change-variant-2/entry')


@app.route('/idp/coin-change-variant-2/<string:name>/')
def coin_change_variant2_simulation(name):
    data = db.coin_change_variant2.find_one({"_id": ObjectId(name)})
    #arr = data['lis_array']
    coin_array1 = ast.literal_eval(data['coin_array_variant2'])
    coin_array2 = []
    coin_array2.append(0)
    for i in range(len(coin_array1)):
        coin_array2.append(int(coin_array1[i]))

    k = len(coin_array1)
    payment = data['payment_variant2']
    l_temp = ccv2.CoinChangeVariant2(int(payment), k , coin_array2)
    data = l_temp.get_data()
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "idp",
                                            "algo": "coin_change_variant2"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/coin_change_variant/coin_change_iterative_dp_variant2_simulation.html', **locals())

