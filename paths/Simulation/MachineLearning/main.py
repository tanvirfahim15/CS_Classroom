from flask import render_template, request, redirect, session, Blueprint
from utility.database import db

app = Blueprint('machine_learning_simulation', __name__)


@app.route('/simulation/ml/')
def machine_learning():
    return render_template(
        '/simulation/machine_learning/index.html', **locals()
    )
