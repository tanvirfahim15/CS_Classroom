from classes.ClassManagement.ConcreteDecorator import ConcreteDecorator

class ageToppings(ConcreteDecorator):


    def __init__(self,age,componentperson):
        self.description=age
        self.componentperson=componentperson;
    

    def getDescription(self):
        info= self.componentperson.getDescription()
        info["Age"]=self.description
        return info



