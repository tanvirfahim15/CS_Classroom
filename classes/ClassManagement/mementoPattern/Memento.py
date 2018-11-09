


class Memento():


    def __init__(self, info,role):
        self.stu_info = {}
        self.tea_info = {}

        if (role == "student"):
            self.stu_info=info
        if (role == "teacher"):
            self.tea_info = info


    def getState(self,role):
        if (role == "student"):
            return self.stu_info

        if (role == "teacher"):
            return self.tea_info