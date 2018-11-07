
import abc


class ComponentPerson(metaclass=abc.ABCMeta):



    info = {}

    @abc.abstractmethod
    def getDescription(self):
        pass








