from flask import Flask, render_template
from paths.Auth import app as auth
from paths.Profile import app as profile
from paths.Simulation.MachineLearning.main import app as machine_learning_simulation
from paths.Simulation.MachineLearning.LinearRegression import app as linear_regression
from paths.Simulation.MachineLearning.LogisticRegression import app as logistic_regression
from paths.Simulation.MachineLearning.KMeansClustering import app as k_means_clustering
from paths.Blog.Write import app as online_forum
from paths.Blog.Read import app as blog_read
from paths.Blog.Subscription import app as blog_subscription

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
app.register_blueprint(blog_read)
app.register_blueprint(blog_subscription)

@app.route("/")
def home():
    return render_template(
        'home.html', **locals())


if __name__ == "__main__":
    app.run()
