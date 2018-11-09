import abc
from pattern.QuizDecoratorPatterm.BasicQuiz import BasicQuiz


class CodimentDecorator(BasicQuiz):
    basic_quiz=None
    question =None

    def set_question(self, question):
        pass


class ConcreteCodiment(CodimentDecorator):

    def __init__(self, basic_quiz, question):
        self.basic_quiz = basic_quiz
        self.set_question(question)
        return

    def set_question(self, question):
        self.question = question
        return

    def add_more_question(self):
        self.question_list = self.basic_quiz.add_more_question()
        self.quiz_name = self.basic_quiz.get_quiz_name()
        self.question_list.append(self.question)
        return self.question_list

    def get_quiz_name(self):
        return self.quiz_name

