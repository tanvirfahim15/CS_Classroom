import flask_login
from flask import Flask, render_template, session, flash
from flask_login import LoginManager

from Database.database import db
from paths.Auth import app as auth
from paths.Profile import app as profile
from paths.Simulation.MachineLearning.main import app as machine_learning_simulation
from paths.Simulation.MachineLearning.LinearRegression import app as linear_regression
from paths.Simulation.MachineLearning.LogisticRegression import app as logistic_regression
from paths.Simulation.MachineLearning.KMeansClustering import app as k_means_clustering
from paths.Blog.Write import app as online_forum
from paths.Blog.Read import app as blog_read
from paths.Blog.Subscription import app as blog_subscription
from paths.CodeGenerator import app as code_generator
import utility.flask_loginmanager as log
from paths.OnlineIde.ide import app as online_ide
from paths.Simulation.IterativeDp.KnapsackApp import app as knpsack
from paths.Simulation.IterativeDp.main import app as iterative_dp_simulation
from paths.Simulation.IterativeDp.EditDistanceApp import app as edit_distance
from paths.Simulation.IterativeDp.LISApp import app as lis
from paths.Simulation.IterativeDp.FibonacciApp import app as dpfib
from paths.Simulation.IterativeDp.LCS import app as lcs
from paths.OnlineClassroom.ClassroomFeed import app as classroom_feed
from paths.Simulation.LinearAlgebra.GaussElimination import app as gauss_elimination


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

log.login_manager.init_app(app)

# Online Editor paths
app.register_blueprint(online_ide)

# Code generator paths
app.register_blueprint(code_generator)

# Iterative Dp paths
app.register_blueprint(iterative_dp_simulation)
app.register_blueprint(knpsack)
app.register_blueprint(edit_distance)
app.register_blueprint(lis)
app.register_blueprint(dpfib)
app.register_blueprint(lcs)

# Linear Algebra Path
app.register_blueprint(gauss_elimination)


# Online Classroom
app.register_blueprint(classroom_feed)

@app.route("/")
def home():
    return render_template(
        'home.html', **locals())


if __name__ == "__main__":
    app.run()
