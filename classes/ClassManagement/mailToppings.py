from classes.ClassManagement.ConcreteDecorator import ConcreteDecorator


class mailToppings(ConcreteDecorator):


    def __init__(self, email, componentperson):
        self.description = email
        self.componentperson = componentperson;

        print("setting mail"+email)


    # def getDescription(self):
    #     return self.description+" "+self.componentperson.getDescription()


    def getDescription(self):
        info= self.componentperson.getDescription()
        info["Email"]=self.description
        return info


