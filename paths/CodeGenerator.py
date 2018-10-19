from flask import render_template, Blueprint

app = Blueprint('code_generator', __name__)


@app.route("/code-generator/")
def code_generator():
    return render_template(
        'code_generator/code_generator.html', **locals())