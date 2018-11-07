import abc


class IMediator(metaclass=abc.ABCMeta):


    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def set(self, component, db, value):
        pass
