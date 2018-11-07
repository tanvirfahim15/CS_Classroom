from classes.ClassManagement.mediatorpattern.Mediator import Mediator

mediator= Mediator()

def getMediatorInstance():
    global mediator

    if(mediator==None):
        mediator =Mediator()
        print("creating object")
    else:
        mediator.x=mediator.x+1
        print("Getting reference ")
        print(mediator.x)


    return mediator
