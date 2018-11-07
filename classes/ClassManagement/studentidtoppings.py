from classes.ClassManagement.ConcreteDecorator import ConcreteDecorator


class studentidtoppings(ConcreteDecorator):


    def __init__(self, id, componentperson):
        self.description = id
        self.componentperson = componentperson



    # def getDescription(self):
    #     return self.description+" "+self.componentperson.getDescription()

    def getDescription(self):
        # print("IdTop->")
        info= self.componentperson.getDescription()
        info["Id"]=self.description
        return info

