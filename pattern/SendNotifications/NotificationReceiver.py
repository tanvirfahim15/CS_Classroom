import abc
from Database.database import db


class Observer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self):
        pass


class Receiver(Observer):
    notifications =""
    user_id = ""

    def __init__(self, user_id , notifications):
        self.user_id = user_id
        self.notifications = notifications

    def update(self):
        user = db.notifications.find_one({'user_id': self.user_id})
        user['notifications'].append(self.notifications)
        return
