from flask import render_template, request, redirect, session, Blueprint
from utility.database import db
from classes.Simulation.MachineLearning.KMeansClustering import KMeansClustering as km
from classes.Simulation.MachineLearning.KMeansClustering import Utility as km_util
import random
from bson import ObjectId

app = Blueprint('k_means_clustering', __name__)


@app.route('/simulation/ml/k-means-clustering/')
def k_means_clustering():
    name = '5b8842c376cc9d18036c6eb4'
    data = db.k_means_clustering.find_one({"_id": ObjectId(name)})
    data = data['data']
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "km"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/machine_learning/k_means_clustering/k_means_clustering_simulation.html', **locals()
    )


@app.route('/simulation/ml/k-means-clustering/<string:name>')
def k_means_clustering_simulation(name):
    data = db.k_means_clustering.find_one({"_id": ObjectId(name)})
    data = data['data']
    saved = 0
    if 'username' in session.keys():
        key = db.saved_simulation.find_one({'algo_id': name, "username": session['username'], "type": "ml",
                                            "algo": "km"})
        if key is not None:
            saved = 1
    return render_template(
        'simulation/machine_learning/k_means_clustering/k_means_clustering_simulation.html', **locals()
    )


@app.route('/simulation/ml/k-means-clustering/entry')
def k_means_clustering_entry(data=None):
    return render_template(
        'simulation/machine_learning/k_means_clustering/k_means_clustering_entry.html', **locals()
    )


@app.route('/simulation/ml/k-means-clustering/entry-data', methods=['POST', 'GET'])
def k_means_clustering_entry_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        if km_util.validate_entry(data['entry']) is False:
            return k_means_clustering_entry(data)

        points = km_util.get_points(data['entry'])
        max_p = 0.0
        min_p = 0.0
        for point in points:
            for entry in point:
                if max_p < entry:
                    max_p = entry
                if min_p > entry:
                    min_p = entry
        centroids = [[random.uniform(min_p, max_p), random.uniform(min_p, max_p)] for i in range(int(data['clusters']))]
        k = km.KMeans(points, centroids)
        data = dict()
        data['data'] = k.get_data()
        posts = db.k_means_clustering
        post_id = posts.insert_one(data).inserted_id
        return redirect('simulation/ml/k-means-clustering/' + str(post_id))


@app.route('/simulation/ml/k-means-clustering/entry-data-sample')
def k_means_clustering_entry_data_sample():
    points = [[1.0, 2.0], [2.0, 2.0], [-5.0, 6.0], [-6.0, 5.0], [7.0, 8.0], [6.0, 5.0]]
    centroids = [[-1.0, 2.0], [-20.0, 2.0], [5.5, 6.6]]
    k = km.KMeans(points, centroids)
    data = dict()
    data['data'] = k.get_data(10)
    posts = db.k_means_clustering
    post_id = posts.insert_one(data).inserted_id
    return redirect('/simulation/ml/k-means-clustering/' + str(post_id))

