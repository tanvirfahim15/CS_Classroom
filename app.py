from flask import Flask, render_template
from utility.database import db
from paths.Auth import app as auth
from paths.Profile import app as profile
from paths.Simulation.MachineLearning.main import app as machine_learning_simulation
from paths.Simulation.MachineLearning.LinearRegression import app as linear_regression
from paths.Simulation.MachineLearning.LogisticRegression import app as logistic_regression
from paths.Simulation.MachineLearning.KMeansClustering import app as k_means_clustering
from paths.Tutorial.OnlineForum.ForumArticle import app as online_forum

app = Flask(__name__)
app.secret_key = 'UIBBN*E(DNJ'

app.register_blueprint(auth)
app.register_blueprint(profile)

# Simulation paths
app.register_blueprint(machine_learning_simulation)
app.register_blueprint(linear_regression)
app.register_blueprint(logistic_regression)
app.register_blueprint(k_means_clustering)

# Online Forum paths
app.register_blueprint(online_forum)

@app.route("/")
def home():
    return render_template(
        'home.html', **locals())


if __name__ == "__main__":
    app.run(debug=True)
