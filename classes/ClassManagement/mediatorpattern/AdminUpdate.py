from classes.ClassManagement.mediatorpattern.IComponent import IComponent


class AdminUpdate(IComponent):



    def __init__(self, mediator):
        self.mediator=mediator
        self.access = 0




    def requestUpdate(self, db,value):
        self.mediator.set(self,db,value)


    def update(self,db,value):
        print("atlast Admin update done here")
        db.insert_one(value)
        print("Inserted")

    def pauseUpdate(self):
        self.access = 0

    def resumeUpdate(self):
        self.access = 1

    def checkStatus(self):
        return self.access

    def setStatus(self, val):
        self.access = val;