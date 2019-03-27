# coding=utf-8
from django.shortcuts import render, redirect
from questions.models import Category, Option, UserScore
from django.http import HttpResponseRedirect
from models import Quiz
from django.contrib.auth.models import User
from forms import QuizForm
from questions.forms import AnsweredQuestionForm
import json
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
# Create your views here.

def random_user():
    return User.objects.order_by('?').first()

@login_required
def index(request):
    if request.method == 'POST':

        form = QuizForm(request.POST)
        if form.is_valid(): # TODO: Errors must be handled
            _id = form.cleaned_data["categories"];

            _category = Category.objects.get(id=_id) # TODO: cleaned data must be used
            number_of_questions = 6
            _questions = _category.get_random_questions(number_of_questions)
            if len(_questions) == 0:
                form = QuizForm(request.POST)
                context_data = {'form': form,'error_message': "سوالی در این موضوع وجود ندارد"}
                return render(request, "quiz_index.html", context_data)
            print "random questions:"
            print _questions

            quiz = Quiz(category=_category)
            user1 = User.objects.get(username=request.user)
            quiz.set_user1(user1)
            user2 = User.objects.order_by('?').first()
            while user2 == user1:
                user2 = User.objects.order_by('?').first()
            quiz.set_user2(user2)
            quiz.save()

            quiz.questions = _questions
            quiz.save()

            print quiz.questions.all()

            #for question in _questions:
                # print "question to be added: "
                # print question.question
            #    quiz.add_question(question)

            #quiz.save()
            # print "quiz questions:" + str(quiz.questions)
            # print "quiz id: " + str(quiz.id)


            print user2.email
            email = EmailMessage('new Challenge', 'quizdown.ir/quiz/start?quiz_id=' + `quiz.id`, to=[user2.email])
            email.send()

            request.session['_quiz_id'] = json.dumps(quiz.id)
            request.session['question_index'] = 0
            request.session.save()
            request.session.modified = True
            return redirect('/quiz/start/')
            # start(None, quiz.id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = QuizForm(request.POST)
        context_data = {'form': form}
        return render(request, "quiz_index.html", context_data)

@login_required
def start(request, seen_questions=[], answers=[]):

    # TODO: seen_questions will not erase after a quiz is finished
    # TODO: pass quiz_id mesle adam
    #if request.method == 'POST':
    print request.session.get('_quiz_id')
    if request.session.get('_quiz_id') and request.session.get('_quiz_id') != "":
        _quiz_id = request.session.get('_quiz_id')
        form = AnsweredQuestionForm(request.POST)
        if form.is_valid():

            print "sssssssss=>" + request.POST.get('selected','')
            if(request.POST.get('selected','') != ''):
                answers.append(request.POST.get('selected',''))
                request.session['question_index'] = int(request.session.get("question_index")) + 1


            quiz = Quiz.objects.get(id=_quiz_id)
            questions = quiz.questions.all()
            context_data = {'quiz_id': _quiz_id}
            print "answers : ==============>"
            print answers

            qindex = request.session.get("question_index")
            print qindex
            for q in questions:
                print q

            if qindex == 0:
                print "answers deleted"
                answers = []


            if qindex == len(questions):
                request.session['_answers'] = json.dumps(answers)
                request.session['question_index'] = 0
                answers = []
                print answers
                request.session.save()
                request.session.modified = True
                return redirect("/quiz/end")

            question = questions[int(qindex)]
            context_data['question'] = question

            opt = Option.objects.filter(question=question)
            context_data['option_a'] = opt[0];
            context_data['option_b'] = opt[1];
            context_data['option_c'] = opt[2];
            context_data['option_d'] = opt[3];
            request.session.save()
            request.session.modified = True
            return render(request,'quiz_start.html', context_data)
    else:
        answers = []
        request.session['_quiz_id'] = request.GET.get('quiz_id', '')
        request.session['question_index'] = 0
        print request.GET.get('quiz_id', '')
        request.session.save()
        request.session.modified = True
        return render(request, 'quiz_start.html')


def to_integer_array(str):
    array = [token for token in str if (token == '1' or token == '2' or token == '3' or token == '4'or token == '5'
                                        or token == '6' or token == '7' or token == '8' or token == '9')]
    integer_array = map(int, array)
    return integer_array;


def calculate_score(userAnswers, questions):
    score = 0;
    j = 0
    print "userAnswers: "
    print userAnswers
    print "len(userAnswers): "
    print len(userAnswers)

    for i in range(len(questions)):
        if len(userAnswers) > len(questions):
            userAnswer = userAnswers[i+len(questions)]
        else:
            userAnswer = userAnswers[i]
        questionOptions = Option.objects.filter(question_id=questions[i].id)
        k = 0;
        for option in questionOptions:
            if(option.is_correct):
                index = k + 1;
            k += 1;

        print "user answers:"
        print userAnswer
        if userAnswer == index:
            if j == len(questions) - 1:
                score += 40
            else:
                score += 20
        j += 1
    return score

def calculate_send_result(this_user_score, that_user_score, user_mail):
    print "email ------------------===============> : " + user_mail
    if that_user_score is None:
        return "انتظار"
    else:
        if that_user_score > this_user_score:
            EmailMessage('your challenge resualt', `this_user_score` +'باخت' + `that_user_score`, to=[user_mail]).send()
            return "باخت"
        elif that_user_score == this_user_score:
            EmailMessage('your challenge resualt', `this_user_score` +'مساوی' + `that_user_score`, to=[user_mail]).send()
            return "مساوی"
        else:
            EmailMessage('your challenge resualt', `this_user_score` +'برد' + `that_user_score`, to=[user_mail]).send()
            return "برد"

@login_required
def end(request):
    if request.session.get('_answers') and request.session.get('_answers') != "" and request.session.get('_quiz_id') and request.session.get('_quiz_id') != "":

        _userAnswers = request.session.get('_answers')
        _quiz_id = request.session.get('_quiz_id')


        quiz = Quiz.objects.get(id=_quiz_id)
        questions = quiz.questions.all()
        userAnswers = to_integer_array(_userAnswers)
        score = calculate_score(userAnswers, questions)

        if User.objects.get(username=request.user) == quiz.get_user1():
            quiz.set_user1Score(score)
            other_score = quiz.user2Score
            other_username = quiz.get_user2().username
            result = calculate_send_result(score, quiz.user2Score, quiz.get_user2().email)
            UserScore(user=User.objects.get(username=request.user), category=quiz.category, score=score).save()

        else:
            quiz.set_user2Score(score)
            other_score = quiz.user1Score
            other_username = quiz.get_user1().username
            result = calculate_send_result(score, quiz.user1Score, quiz.get_user1().email)
            UserScore(user=User.objects.get(username=request.user), category=quiz.category, score=score).save()

        quiz.save()


        request.session['_answers'] = ""
        request.session['_quiz_id'] = ""
        request.session.save()
        request.session.modified = True

        return render(request, 'quiz_end.html', {'username1': request.user , 'username2': other_username,
                                                 'score1': score, 'score2': other_score, 'resault': result})
    else:
        return redirect("/quiz/")