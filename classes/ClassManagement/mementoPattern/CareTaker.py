


class CareTaker():

    def __init__(self):
        self.stu_mementos = []
        self.tea_mementos = []
        self.mementos=[]


    def addState(self, mem, role):
        if (role == "student"):
            self.mementos=self.stu_mementos
        if (role == "teacher"):
            self.mementos = self.tea_mementos

        self.mementos.append(mem)


    def getStateFromMemento(self,role):

        if (role == "student"):
            self.mementos = self.stu_mementos
        if (role == "teacher"):
            self.mementos = self.tea_mementos


        size= len(self.mementos)
        print(size)
        ob= self.mementos[size-1]
        self.mementos.remove(ob)
        return ob


    def getMementoSize(self,role):

        if (role == "student"):
            self.mementos = self.stu_mementos
        if (role == "teacher"):
            self.mementos = self.tea_mementos

        return len(self.mementos)