import flask_login
from bson import ObjectId
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, session, Blueprint
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import classes.Blog.Subscription.Writer as Writer
from utility.database import db
import datetime


app = Blueprint('blog_write', __name__)

now = datetime.datetime.now()

@app.route('/articles')
def articles():
    articles = db.article.find()

    if articles is not None:
        return render_template('/tutorial/articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('/tutorial/articles.html', msg=msg)


@app.route('/article/<string:id>/')
def article(id):
    articles = db.article.find({"_id": ObjectId(id)})
    print(articles)
    return render_template('/tutorial/article.html', articles=articles)


@app.route('/dashboard')
def dashboard():
    articles = db.article.find({"author": session['username']})
    print(articles)
    if articles is not None:
        return render_template('/tutorial/dashboard.html', articles=articles)
    else:
        msg = 'You Do Not Have Any Articles'
        return render_template('/tutorial/dashboard.html', msg=msg)


class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=4)])


@app.route('/add_article', methods=['GET', 'POST'])
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        author = session['username']

        article_id = db.article.insert({"title": title, "author": author, "body": body, "date": str(now)})
        article_id = str(article_id)
        flash('Article Created', 'success')
        Writer.Writer(session['username']).notify_observer(article_id)
        return redirect('/article/'+article_id+'/')

    return render_template('/tutorial/add_article.html', form=form)


@app.route('/online_forum/forum_home')
def forum_home():
    return render_template('/tutorial/forum_home.html', **locals())


