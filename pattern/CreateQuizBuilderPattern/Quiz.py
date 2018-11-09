class Quiz:
    question=''
    option1=''
    option2=''
    option3=''
    option4=''
    currect_answer=''


    def __init__(self):
        pass

    class QuizBuilder:
        question = ''
        option1 = ''
        option2 = ''
        option3 = ''
        option4 = ''
        currect_answer = ''

        def __init__(self, question):
            self.question = question

        def with_option1(self, option1):
            self.option1 = option1
            return self

        def with_option2(self, option2):
            self.option2 = option2
            return self

        def with_option3(self, option3):
            self.option3 = option3
            return self

        def with_option4(self, option4):
            self.option4 = option4
            return self

        def with_currect_answer(self, currect_answer):
            self.currect_answer = currect_answer
            return self

        def build(self):
            quiz = Quiz()
            quiz.question = self.question
            quiz.option1 = self.option1
            quiz.option2 = self.option2
            quiz.option3 = self.option3
            quiz.option4 = self.option4
            quiz.currect_answer=self.currect_answer
            return quiz

    def getQuestion(self):
        return self.question

    def getOption1(self):
        return self.option1

    def getOption2(self):
        return self.option2

    def getOption3(self):
        return self.option3

    def getOption4(self):
        return self.option4

    def getCurrectAnswer(self):
        return self.currect_answer


