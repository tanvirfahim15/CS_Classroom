import pattern.ObserverPattern as ObserverPattern
from Database.database import db
import classes.Mail.SendMail as Mail


class MailReciever(ObserverPattern.Observer):
    SUBJECT = "New Article Update from CS Classroom"
    reciever_id = ""

    def __init__(self, reciever):
        self.reciever_id = reciever

    def get_html(self,message):
        writer, article = message
        return writer+" has published new article<br/><a href=\""+"http://csclassroom-sdp.herokuapp.com/article/"+article\
               + "/\">Click here to see</a>"

    def get_text(self, message):
        writer, article = message
        return writer + " has published new article: " + "http://csclassroom-sdp.herokuapp.com/article/" + article \
               + "/"

    def update(self, message):
        writer, article = message
        print(writer)
        print(article)
        user = db.users.find_one({'username': self.reciever_id})
        email = user['email']
        Mail.SendMessage(email, MailReciever.SUBJECT, self.get_html(message), self.get_text(message))

