# Python 3.4+
from classes.ClassManagement.ComponentPerson import ComponentPerson

from abc import ABCMeta
import  six
@six.add_metaclass(ABCMeta)
class ConcreteDecorator(ComponentPerson):

    def __init__(self):
        componentperson = ComponentPerson()

    def getDescription(self):
        return ""




