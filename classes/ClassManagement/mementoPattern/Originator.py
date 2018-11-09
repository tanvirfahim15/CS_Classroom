from classes.ClassManagement.mementoPattern.Memento import Memento


class Originator():

    def __init__(self):
        self.stu_info={}
        self.tea_info={}

    def setState(self, info, role):
        if (role == "student"):
            self.stu_info=info
        if (role == "teacher"):
            self.tea_info = info

        # self.info=info



    def save(self,role):
        mem=None
        if (role == "student"):
            mem = Memento(self.stu_info,role)
        if (role == "teacher"):
            mem = Memento(self.tea_info,role)
        return mem


    def restore(self, mem,role):

        if (role == "student"):
            self.stu_info= mem.getState(role)
        if (role == "teacher"):
            self.tea_info = mem.getState(role)


