from Database.database import db


def blog_profile(id):
    user = db.users.find_one({'username': id})
    articles = db.article.find({"author": id})
    return user, articles
