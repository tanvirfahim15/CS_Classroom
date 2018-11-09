import abc
from pattern.CreateQuizBuilderPattern.Quiz import Quiz

class BasicQuiz(metaclass=abc.ABCMeta):
    quiz_name=''
    question_list = []

    @abc.abstractmethod
    def add_more_question(self):
        pass

    @abc.abstractmethod
    def get_quiz_name(self):
        pass


class ConcreteBasicQuiz(BasicQuiz):

    def __init__(self, quiz_name):
        self.quiz_name = quiz_name
        self.question_list = []

    def add_more_question(self):
        return self.question_list

    def set_quiz_name(self, quiz_name):
        self.quiz_name = quiz_name
        return

    def get_quiz_name(self):
        return self.quiz_name
