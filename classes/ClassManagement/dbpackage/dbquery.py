from Database.database import db


def getAllStudent():
    data = []
    for cou in db.xenrolled_student.find():
        # print(cou)
        data.append(cou)


    return data



def getAllTeacher():
    data = []
    for cou in db.xenrolled_teacher.find():
        # print(cou)
        data.append(cou)

    return data


def getCourseUser():
    data=[]

    for cou in db.courses.find():
        data.append(cou)

    return data