from classes.ClassManagement.mediatorpattern.IComponent import IComponent


from classes.ClassManagement.mediatorpattern.IComponent import IComponent


class TeacherUpdate(IComponent):



    def __init__(self, mediator):
        self.mediator=mediator
        self.access = 0




    def requestUpdate(self, value):
        self.mediator.set(self,value)


    def update(self,db,value):
        print("atlast Teacher update done here")
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