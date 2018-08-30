import json
import numpy as np
from flask import render_template, request, redirect, session, Blueprint
from utility.database import db
from bson.objectid import ObjectId
from classes.Simulation.MachineLearning.LinearRegression import LinearRegression as lr
import classes.Simulation.MachineLearning.LinearRegression.Utility as lr_util

app = Blueprint('linear_regression', __name__)


@app.route('/simulation/ml/linear-regression/')
def linear_regression():
    return redirect('/simulation/ml/linear-regression/5b761a357033b71cc432d99e')


@app.route("/simulation/ml/linear-regression/entry")
def linear_regression_data_entry(data=None):
    return render_template(
        'simulation/machine_learning/linear_regression/linear_regression_entry.html', **locals())


@app.route("/simulation/ml/linear-regression/entry_data", methods=['POST', 'GET'])
def linear_regression_data_entry_data():
    if request.method == 'POST':
        data = request.form
        ret_data = dict()

        try:
            alpha = float(data['alpha'])
        except ValueError:
            ret_data['data']=data['entry'].replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Wrong format for Alpha'
            return linear_regression_data_entry(ret_data)

        try:
            iterations = int(data['iterations'])
        except ValueError:
            ret_data['data']=data['entry'].replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Wrong format for Iterations'
            return linear_regression_data_entry(ret_data)

        try:
            steps = int(data['steps'])
        except ValueError:
            ret_data['data']=data['entry'].replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Wrong format for Steps'
            return linear_regression_data_entry(ret_data)

        try:
            theta0 = float(data['theta0'])
            theta1 = float(data['theta1'])
            theta = np.array([theta0, theta1]);
        except ValueError:
            ret_data['data']=data['entry'].replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Wrong format for Theta'
            return linear_regression_data_entry(ret_data)

        if steps > iterations:
            ret_data['data']=data['entry'].replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Steps should be less than iterations'
            return linear_regression_data_entry(ret_data)

        if iterations%steps!=0:
            iterations -= iterations%steps

        if iterations/steps > 30:
            ret_data['data']=data['entry'].replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Either decrease iterations or increase steps.'
            return linear_regression_data_entry(ret_data)

        data = str(json.dumps(data['entry'])).replace("\"", "")
        if lr_util.validate_entry(data) is False:
            ret_data['data']=data.replace('\"', '').replace('\\r\\n', '\n')
            ret_data['msg'] = 'Wrong Data Format'
            return linear_regression_data_entry(ret_data)

        ret_data['data'] = data.replace('\"', '').replace('\\r\\n', '\n')
        ret_data['msg'] = 'Overshoot occurred. Try lower value of Alpha.'
        data = lr_util.get_matrix(data)

        x = data[0]
        y = data[1]
        x = np.asarray(x)
        y = np.asarray(y)

        ln = lr.LinearRegression(theta, x, y, alpha, iterations, steps)
        data = ln.get_dictionary()

        if data['overshoot']:
            return linear_regression_data_entry(ret_data)
        posts = db.linear_regression
        post_id = posts.insert_one(data).inserted_id
        return redirect('/simulation/ml/linear-regression/' + str(post_id))


@app.route('/simulation/ml/linear-regression/<string:name>')
def linear_regression_simulation(name):
    data = db.linear_regression.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "lr"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/machine_learning/linear_regression/linear_regression_simulation.html', **locals())

