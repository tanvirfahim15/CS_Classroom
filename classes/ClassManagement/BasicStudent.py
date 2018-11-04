from classes.ClassManagement.ComponentPerson import ComponentPerson


class BasicStudent(ComponentPerson):
    def __init__(self):
        ComponentPerson.__init__(self)

    def getDescription(self):
        info={}
        info["Person"] = "Student"
        return info


