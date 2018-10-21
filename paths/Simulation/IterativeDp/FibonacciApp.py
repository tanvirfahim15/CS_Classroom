from bson import ObjectId
from flask import render_template, request, redirect, session, app, Blueprint
from Database.database import db

import classes.Simulation.IterativeDp.Fibonacci as dpfib

app = Blueprint('dpfib', __name__)

@app.route("/idp/fib")
def fib():
    data = dpfib.Fibonacci(30)
    data = data.get_data()
    return render_template(
        '/simulation/fibonacci_iterative_dp/fibonacci.html', **locals()
    )