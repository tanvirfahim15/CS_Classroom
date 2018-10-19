from flask import render_template, session, Blueprint
from Database.database import db
import classes.Blog.Subscription.Writer as Writer_Subject
from Service.Blog import Read as service

app = Blueprint('blog_read', __name__)


@app.route('/blog/profile/<string:id>/')
def blog_profile(id):
    user, articles = service.blog_profile(id)
    subscribed = Writer_Subject.Writer(id).find_observer(session['username'])
    return render_template('/blog/profile.html', **locals())

# blog/profile
# blog/newsfeed
# blog/view article