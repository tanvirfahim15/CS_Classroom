from classes.ClassManagement.ComponentPerson import ComponentPerson


class BasicTeacher(ComponentPerson):
    def __init__(self):
        ComponentPerson.__init__(self)

        def getDescription(self):
            info = {}
            info["Person"] = "Teacher"
            return info



