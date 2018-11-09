import abc
from Database.database import db


class CommentObserver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self):
        pass


class CommentReceiver(CommentObserver):
    notifications =""
    user_id = ""

    def __init__(self, user_id , notifications):
        self.user_id = user_id
        self.notifications = notifications

    def update(self):
        user = db.notifications.find_one({'username': self.user_id})
        if user is None:
            data = {'username':self.user_id, 'notifications':[]}
            db.notifications.insert_one(data)
            user = db.notifications.find_one({'username': self.user_id})

        user['notifications'].append(self.notifications)
        db.notifications.replace_one({'username':self.user_id} , user)
        return
