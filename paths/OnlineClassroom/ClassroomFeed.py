from flask import Blueprint
from flask import render_template, request, redirect, session,jsonify,flash
from Service.OnlineClassroom import ClassroomFeed as service
from pattern.AdapterPattern.addclasstopost import addclasstopost
from pattern.AdapterPattern.assignmenttopost import assignmenttopost
from pattern.CreateQuizBuilderPattern.Quiz import Quiz
from pattern.QuizDecoratorPatterm.BasicQuiz import ConcreteBasicQuiz
from pattern.QuizDecoratorPatterm.DecoratorQuiz import ConcreteCodiment
from pattern.GiveAQuizDecoratorPattern.DecoratorGiveQuiz import CodimentGiveDecorator,ConcreteGiveCodiment
from pattern.GiveAQuizDecoratorPattern.BasicGiveQuiz import BasicGiveQuiz,ConcreteBasicGiveQuiz

from classes.OnlineClassroom.Answer import Answer
app = Blueprint('classroom_feed', __name__)

global_quiz = ConcreteBasicQuiz(None)
global_answer= ConcreteBasicGiveQuiz(None)

@app.route("/news-feed/<course_id>")
def show_news_feed(course_id):
    enrolled_flag = service.check_is_enrolled(course_id)
    if enrolled_flag == -1:
        flash('You are not enrolled. Join the class please.')
        return redirect('/classroom-courses-dashboard')
    course_info, data, users, notifications = service.show_news_feed(course_id)
    classmate_count = len(course_info['enrolled'])
    quiz_list = service.get_quiz_lists(course_id)
    return render_template('OnlineClassroom/post_and_comment/feed.html', **locals())


@app.route("/entry_data/<course_id>" , methods=['POST', 'GET'])
def update_post(course_id):
    if request.method=="POST":
        data = request.form
        # print(data)
        if len(data['message']) != 0:
            service.update_post(data , course_id)
        else:
            flash("Post is empty!! Write something..")
    return redirect('/news-feed/'+str(course_id))


@app.route("/comment_entry/<id>/<course_id>" , methods=['POST', 'GET'])
def comment_entry(id, course_id):
    poststring , comments , course_info , notifications= service.comment_entry(id, course_id)
    classmate_count = len(course_info['enrolled'])
    return render_template('OnlineClassroom/post_and_comment/comment.html' ,**locals())


@app.route("/entry_comment/<id>/<course_id>/<author>" , methods=['POST', 'GET'])
def update_comment(id, course_id,author):
    print(id+" "+course_id+" "+author)
    if request.method=="POST":
        data = request.form
        service.update_comment(id ,course_id,data,author)

    return redirect('/comment_entry/'+str(id)+'/'+str(course_id))


@app.route("/assignment/<course_id>")
def assingmnet(course_id):
    return render_template('OnlineClassroom/post_and_comment/giveassignment.html', **locals())


@app.route('/add_assignment/<course_id>')
def add_assignment(course_id):
    time = request.args.get('time', 0, type=str)
    date = request.args.get('date', 0, type=str)
    details= request.args.get('details', 0, type=str)
    # print(time)
    # print(date)
    # print(details)
    assignmenttopost(time,date,details,session['username'],course_id)
    return jsonify(result="assignment added")


@app.route('/class/<course_id>')
def class_add(course_id):
    return render_template('OnlineClassroom/post_and_comment/addclass.html', **locals() )


@app.route('/add_class/<course_id>')
def add_class(course_id):
    starttime = request.args.get('starttime', 0, type=str)
    endtime = request.args.get('endtime', 0, type=str)
    details= request.args.get('details', 0, type=str)
    # print(starttime)
    # print(endtime)
    # print(details)
    addclasstopost(starttime,endtime,details,session['username'],course_id)
    return jsonify(result="new class time has been announced")


@app.route('/give_mcq/<course_id>/<quiz_id>')
def give_mcq(course_id, quiz_id):
    curse=service.get_quiz_data(quiz_id)
    # print("in app route")
    # print(curse)
    data=curse['questions']
    qno=0
    global global_answer
    global_answer=None
    global_answer=ConcreteBasicGiveQuiz(curse['quiz_name'])
    # print(global_answer.question_list)
    return render_template('OnlineClassroom/post_and_comment/give_mcq.html', **locals())


@app.route('/re_next_mcq/<quiz_id>/<qno>/<course_id>')
def re_next_mcq(quiz_id, qno, course_id):
    curse = service.get_quiz_data(quiz_id)
    qno = int(qno)
    data = curse['questions']
    return render_template('OnlineClassroom/post_and_comment/give_mcq.html', **locals())


@app.route('/next_mcq/<quiz_id>/<qno>/<course_id>/<question>',methods=['POST','GET'])
def next_mcq(quiz_id,qno,course_id,question):
    if request.method=="POST":
        answerdata = request.form
        flag_is_answered = service.check_is_answer_selected(answerdata)
        if flag_is_answered == -1:
            flash("Please Choose an Option.")
            return redirect('/re_next_mcq/'+str(quiz_id)+'/'+str(qno)+'/'+str(course_id))
        curse = service.get_quiz_data(quiz_id)
        data=curse['questions']
        qno=int(qno)
        qno+=1
        # print('answerdata')
        # print(answerdata)
        answer=Answer(question,answerdata['radioName1'])
        global global_answer
        global_answer = ConcreteGiveCodiment(global_answer, answer)
    return render_template('OnlineClassroom/post_and_comment/give_mcq.html', **locals())


@app.route('/create_mcq/<c_id>')
def create_mcq(c_id):
    course_id=c_id
    qno=0
    return render_template('OnlineClassroom/post_and_comment/add_quiz_name.html',**locals())


@app.route('/add_quiz_name/<c_id>', methods=['POST', 'GET'])
def add_quiz_name(c_id):
    if request.method=='POST':
        data = request.form
        course_id = c_id
        qno = 1
        # print('add_quiz_name:')
        # print(data['name'])
        if len(data['name']) == 0:
            flash('Please Add a Quiz name')
            return redirect('/create_mcq/'+str(course_id))
        global global_quiz
        global_quiz = ConcreteBasicQuiz(data['name'])
    return render_template('OnlineClassroom/post_and_comment/create_mcq.html', **locals())


@app.route('/re_create_question/<course_id>/<qno>')
def re_create_question(course_id, qno):
    return render_template('OnlineClassroom/post_and_comment/create_mcq.html', **locals())


@app.route('/create_question/<qno>/<course_id>' , methods=['POST', 'GET'])
def create_question(qno,course_id):
    if request.method=="POST":
        data = request.form
        # print(data)
        flag_for_all = service.check_is_all_field_fill_up(data)
        if flag_for_all == -1:
            flash('Please fill up all fields.')
            return redirect('/re_create_question/'+str(course_id)+'/'+str(qno))
        quiz = Quiz.QuizBuilder(data['question'])\
            .with_option1(data['option1'])\
            .with_option2(data['option2'])\
            .with_option3(data['option3'])\
            .with_option4(data['option4'])\
            .with_currect_answer(data['radioName'])\
            .build()
        # print(quiz)
        global global_quiz
        global_quiz = ConcreteCodiment(global_quiz, quiz)

        qno=int(qno)
        qno+=1
        # print(qno)
    return render_template('OnlineClassroom/post_and_comment/create_mcq.html',**locals())


@app.route('/create_last_question/<qno>/<course_id>' , methods=['POST', 'GET'])
def create_last_question(qno,course_id):
    if request.method=="POST":
        data = request.form
        # print(data)
        flag_for_all = service.check_is_all_field_fill_up(data)
        if flag_for_all == -1:
            flash('Please fill up all fields.')
            return redirect('/re_create_question/' + str(course_id) + '/' + str(qno))
        quiz = Quiz.QuizBuilder(data['question']) \
            .with_option1(data['option1']) \
            .with_option2(data['option2']) \
            .with_option3(data['option3']) \
            .with_option4(data['option4']) \
            .with_currect_answer(data['radioName']) \
            .build()
        global global_quiz
        global_quiz = ConcreteCodiment(global_quiz, quiz)
        service.save_quiz_to_databse(global_quiz, course_id)
        qno=int(qno)
        qno+=1
        # print(qno)
        # print(course_id)
    return render_template('OnlineClassroom/post_and_comment/successfully_quiz_created.html',**locals())


@app.route('/quiz_result/<quiz_id>/<qno>/<course_id>/<question>' , methods=['POST', 'GET'])
def quiz_result(quiz_id,qno,course_id,question):
    if request.method=="POST":
        answerdata = request.form
        flag_is_answered = service.check_is_answer_selected(answerdata)
        if flag_is_answered == -1:
            flash("Please Choose an Option.")
            return redirect('/re_next_mcq/' + str(quiz_id) + '/' + str(qno) + '/' + str(course_id))
        curse = service.get_quiz_data(quiz_id)
        data=curse['questions']
        # print('answerdata')
        # print(answerdata)
        answer=Answer(question,answerdata['radioName1'])
        global global_answer
        global_answer = ConcreteGiveCodiment(global_answer, answer)
        list=global_answer.add_more_question()
        # for answer in list:
        #     print(answer.get_question(),answer.get_answer())
        score=calculate_score(data,list)
    return render_template('OnlineClassroom/post_and_comment/quiz_result.html',**locals())


def calculate_score(data, list):
    # print("calculate score")
    # print(data)
    # print(list)
    score = 0
    for i in range(0,5):
        # print(data[i]['correct_answer']+" "+list[i].get_answer())
        if data[i]['correct_answer'] == list[i].get_answer():
            score += 20
    # print("calculate score")
    # print(score)
    return score