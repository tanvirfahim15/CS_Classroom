class post:

    def __init__(self,posttext,postfile,authors):
        self.posttext=posttext
        self.postfile=postfile
        self.authors=authors
    def getdescription(self):
        return {"posttext": posttext, "postfile": postfile , "authors": authors}
        posts = db.hello_world123
        post_id = posts.insert_one(data).inserted_id
        return