from classes.ClassManagement.mediatorpattern.AdminUpdate import AdminUpdate
# from classes.ClassManagement.mediatorpattern.IComponent import IMediator
from classes.ClassManagement.mediatorpattern.IMediator import IMediator
from classes.ClassManagement.mediatorpattern.StudentUpdate import StudentUpdate
from classes.ClassManagement.mediatorpattern.TeacherUpdate import TeacherUpdate


class Mediator(IMediator):



    def __init__(self):
        self.adminUpdate = AdminUpdate(self)
        self.studentUpdate = StudentUpdate(self)
        self.teacherUpdate = TeacherUpdate(self)
        self.x=0



    def set(self, component, db, value):
        if isinstance(component, AdminUpdate):
            print("in set and checking instanceof")
            self.setadminUpdate(db,value)

        if isinstance(component, StudentUpdate):
            self.setstudentUpdate(db,value)

        if isinstance(component, TeacherUpdate):
            self.setteacherUpdate(db,value)





    def setadminUpdate(self, db, value):
       #  check conditions

       # print("checking conditions: ")
       # print(self.teacherUpdate.checkStatus())
       # print(self.studentUpdate.checkStatus())
       # print()
       if self.teacherUpdate.checkStatus() == 0 and self.studentUpdate.checkStatus() == 0:
           self.teacherUpdate.pauseUpdate()
           self.studentUpdate.pauseUpdate()

           print("setting admin Update with conditions")
           self.adminUpdate.setStatus(1)
           self.adminUpdate.update(db,value)
           self.adminUpdate.setStatus(0)

           self.teacherUpdate.resumeUpdate()
           self.studentUpdate.resumeUpdate()



    def setstudentUpdate(self,db,value):
        if self.teacherUpdate.checkStatus() == 0 and self.adminUpdate.checkStatus() == 0:
            self.teacherUpdate.pauseUpdate()
            self.adminUpdate.pauseUpdate()

            self.studentUpdate.setStatus(1)
            self.studentUpdate.update(db,value)
            self.studentUpdate.setStatus(0)

            self.teacherUpdate.resumeUpdate()
            self.adminUpdate.resumeUpdate()



    def setteacherUpdate(self,db,value):
        if self.adminUpdate.checkStatus() == 0 and self.studentUpdate.checkStatus() == 0:
            self.adminUpdate.pauseUpdate()
            self.studentUpdate.pauseUpdate()

            self.teacherUpdate.setStatus(1)
            self.teacherUpdate.update(db,value)
            self.teacherUpdate.setStatus(0)

            self.adminUpdate.resumeUpdate()
            self.studentUpdate.resumeUpdate()

