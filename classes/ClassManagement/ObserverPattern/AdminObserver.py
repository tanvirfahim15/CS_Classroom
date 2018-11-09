from classes.ClassManagement.ObserverPattern.IEnrollmentObserver import IEnrollmentObserver
from flask import Blueprint
from bson import ObjectId
from flask import Flask, render_template, request, redirect, session
from Database.database import db
from Service.OnlineClassroom import ClassroomHome as service

class AdminObserver(IEnrollmentObserver):

    def __init__(self):
        pass


    def update(self, studentEnroll, techerCreateClass):
        print('here printing admin update')
        print(studentEnroll)
        print(techerCreateClass)


        if studentEnroll: #need work a little
            enroll_stu = db.xenrolled_student
            enroll_stu.insert_one(studentEnroll)

        if techerCreateClass:
            service.create_class_info_update(techerCreateClass)

        return

