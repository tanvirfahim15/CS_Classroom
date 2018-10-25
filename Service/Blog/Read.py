from Database.database import db
import classes.Blog.Subscription.Writer as Writer_Subject
from flask import session
from bson import ObjectId


def blog_profile(id):
    user = db.users.find_one({'username': id})
    articles = db.article.find({"author": id})
    if 'username' in session.keys():
        subscribed = Writer_Subject.Writer(id).find_observer(session['username'])
    else:
        subscribed = False
    own = None
    if session['username'] == id:
        own = True
    return user, articles, subscribed, own


def blog_newsfeed():
    writers = []
    for writer in db.subsription.find():
        if session['username'] in writer['readers']:
            writers.append(writer['writer_id'])
    articles = []
    for writer in writers:
        article_s=db.article.find( { 'author' : writer })
        for article in article_s:
            articles.append(article)
    articles = sorted(articles, key=lambda k: k['date'],reverse=True)
    return articles


def blog_qpredict(id):
    return db.article.find_one({"_id": ObjectId(id)})['body']

