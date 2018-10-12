from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, Blueprint
from utility.database import db


app = Blueprint('blog_read', __name__)


@app.route('/blog/profile/<string:id>/')
def blog_profile(id):
    user = db.users.find_one({'username': id})
    articles = db.article.find({"author": id})
    return render_template('/blog/profile.html', **locals())

# blog/profile
# blog/newsfeed
# blog/view article