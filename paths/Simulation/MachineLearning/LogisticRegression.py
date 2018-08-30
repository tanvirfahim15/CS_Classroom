from flask import render_template, request, redirect, session, Blueprint
from utility.database import db
from classes.Simulation.MachineLearning.LogisticRegression import LogisticRegression as lgr
from classes.Simulation.MachineLearning.LogisticRegression import Utility as lgr_util
import numpy as np
from bson import ObjectId

app = Blueprint('logistic_regression', __name__)


@app.route('/simulation/ml/logistic-regression')
def logistic_regression():
    name = '5b76a9627033b703f464b308'
    data = db.logistic_regression.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    max_iter = len(data['data'])/5
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "lgr"})
        if key is not None:
            saved = 1
    return render_template(
        '/simulation/machine_learning/logistic_regression/logistic_regression_simulation.html', **locals()
    )


@app.route('/simulation/ml/logistic-regression/<string:name>')
def logistic_regression_simulation(name):
    data = db.logistic_regression.find_one({"_id": ObjectId(name)})
    data.pop('_id')
    max_iter = len(data['data'])/5
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "lgr"})
        if key is not None:
            saved = 1
    return render_template(
        '/simulation/machine_learning/logistic_regression/logistic_regression_simulation.html', **locals()
    )


@app.route('/simulation/ml/logistic-regression/entry')
def logistic_regression_data_entry(data=None):
    return render_template(
        '/simulation/machine_learning/logistic_regression/logistic_regression_entry.html', **locals()
    )


@app.route('/simulation/ml/logistic-regression/entry-data', methods=['POST', 'GET'])
def logistic_regression_data_entry_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        if lgr_util.validate_entry(data) is False:
            return logistic_regression_data_entry(data)
        iterations = int(data['iterations'])
        steps = int(data['steps'])
        alpha = float(data['alpha'])
        data = lgr_util.get_data(data['entry'])
        x1 = data[0]
        x2 = data[1]
        y = np.asarray(data[2])
        x = lgr_util.combine(x1, x2)
        l = lgr.LogisticRegression(x, y)
        data = dict()
        data['data'] = l.get_data(iterations, steps, alpha)
        data['x1'] = x1
        data['x2'] = x2
        data['y'] = list(y)
        data['alpha'] = alpha
        posts = db.logistic_regression
        post_id = posts.insert_one(data).inserted_id
        return redirect('/simulation/ml/logistic-regression/' + str(post_id))
