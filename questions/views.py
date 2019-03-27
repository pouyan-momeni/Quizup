# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import serializers
from django.http.response import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.http import HttpResponse
from questions.forms import QuestionForm, CategoryForm
from questions.models import Question, Option, Category, UserScore
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


def get_options_for_questions(questions):
    options = []
    for question in questions:
        opt = Option.objects.filter(is_correct=True, question=question)
        if not opt:
            opt = u"ندارد"
        else:
            opt = opt[0]
        options.append((question, opt))
    return options


def get_all_questions():
    questions = Question.objects.all()
    options = get_options_for_questions(questions)
    context_data = {'questions': questions, 'options': options}
    return context_data


def get_all_categories():
    return Category.objects.all()


def get_question_by_category(category):
    questions = Question.objects.filter(category=category)
    options = get_options_for_questions(questions)
    context_data = {'questions': questions, 'options': options}
    return context_data


def get_category_by_name(name):
    return Category.objects.filter(name=name)


def get_default_top_score_list():
    unknown = u'نامشخص'
    top_users = [(unknown, 0), (unknown, 0), (unknown, 0)]
    return top_users


@login_required
def show_ranking(request, category_id):
    score = 0
    if not category_id:
        category_name = u'همه'
        user_scores = UserScore.objects.filter(user=request.user)
        top_users_score = UserScore.objects.all().order_by('-score')  # wrong query for test
    else:
        category_name = Category.objects.get(id=category_id).name
        user_scores = UserScore.objects.filter(user=request.user, category__id=category_id)
        top_users_score = UserScore.objects.filter(category__id=category_id).order_by('-score')

    for user_score in user_scores:
        score += user_score.score

    user_rank = 1
    for top_user in top_users_score:
        if top_user.score == score:
            break
        user_rank += 1

    top_users = get_default_top_score_list()
    for i in range(0, 3):
        if i < len(top_users_score):
            top_users[i] = (top_users_score[i].user, top_users_score[i].score)

    context_data = {'category': category_name, 'user_score': score, 'user_rank': user_rank, 'top_users': top_users}
    return render(request, 'show_ranking.html', context_data)


# @login_required
# def index(request):
#     if request.method == 'GET':
#         context_data = get_all_questions()
#         context_data['cat_name'] = u'همه'
#         return render(request, 'questions_index.html', context_data)
#     elif request.POST.get(u'action') == u'ویرایش':
#         question = Question.objects.filter(question=request.POST.get(u'question'))
#         options = Option.objects.filter(question=question)
#         context_data = {'question': question[0], "options": options,
#                         "form": QuestionForm(), "done": False}
#         return render(request, 'edit_question.html', context_data)
#     elif request.POST.get(u'action') == u'حذف':
#         Question.objects.filter(question=request.POST.get(u'question')).delete()
#         context_data = get_all_questions()
#         context_data['cat_name'] = u'همه'
#         return render(request, 'questions_index.html', context_data)


@login_required
def view_question(request):
    pass


@login_required
def show_category(request, category_id):
    if request.method == 'GET':
        all_categories = get_all_categories()
        context_data = get_question_by_category(Category.objects.get(id=category_id))
        context_data['categories'] = all_categories
        context_data['showing_id'] = int(category_id)
        return render(request, 'categories_index.html', context_data)
    elif request.POST.get('add') != None:
        return HttpResponseRedirect('/questions/add_category')
    elif request.POST.get(u'action') == u'ویرایش':
        request.session['question_before_edit_id'] = Question.objects.filter(question = request.POST.get('question'))[0].question
        options = Option.objects.filter(question = Question.objects.filter(question = request.POST.get('question'))[0])
        short_options = []
        for option in options:
            short_options.append({'text':option.text, 'is_correct':option.is_correct})

        request.session['options_for_question_before_edit'] = short_options
        request.session.save()
        form = QuestionForm()
        context_data = {'question': Question.objects.filter(question = request.POST.get('question'))[0],
                        "options": options, 'showing_id':int(category_id), "category": Category.objects.get(id=category_id),
                        'form': form, "done": False}
        return render(request, 'edit_question.html', context_data)
    elif request.POST.get(u'action') == u'حذف':
        question = Question.objects.filter(question = request.POST.get('question'))[0]
        options = Option.objects.filter(question = question)
        for option in options:
            option.delete()

        question.delete()
        context_data = {'categories' : get_all_categories(), 'showing_id':int(category_id)}
        return render(request, 'categories_index.html', context_data)
    else:
        context_data = get_question_by_category(get_category_by_name(name=request.POST.get('cat_name')))
        context_data['cat_name'] = request.POST.get('cat_name')
        return render(request, 'questions_index.html', context_data)


@login_required
def show_categories(request):
    all_categories = get_all_categories()
    if len(all_categories):
        return redirect(reverse('show_category', args=str(all_categories[0].id)))
    else:
        return redirect('/add_category/')

def get_category_page_parameters(done, error_message, form):
    return {'form': form, "done": done, 'error_message': error_message}


@login_required
def create_a_category(request):
    done = False
    error_message = ""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = Category(name=category_name)
            category.save()
            done = True
        else:
            error_message = u"این نام قبلا استفاده شده‌است"
    else:
        form = CategoryForm()

    context_data = get_category_page_parameters(done, error_message, form)
    return render(request, 'add_category.html', context_data)


def create_question_from_form(category_id, form, request):
    question = Question()
    question.question = form.cleaned_data['question_text']
    question.category = Category.objects.get(id=category_id)
    question.creator = request.user
    options = []
    options.append(Option(text=form.cleaned_data.get('a', 'Unspecified Option Text'),
                          is_correct=form.cleaned_data.get('a_is_correct', False),
                          question=question
                          )
                   )
    options.append(Option(text=form.cleaned_data.get('b', 'Unspecified Option Text'),
                          is_correct=form.cleaned_data.get('b_is_correct', False),
                          question=question
                          )
                   )
    options.append(Option(text=form.cleaned_data.get('c', 'Unspecified Option Text'),
                          is_correct=form.cleaned_data.get('c_is_correct', False),
                          question=question
                          )
                   )
    options.append(Option(text=form.cleaned_data.get('d', 'Unspecified Option Text'),
                          is_correct=form.cleaned_data.get('d_is_correct', False),
                          question=question
                          )
                   )
    return options, question


@login_required
def create_a_question(request, category_id):
    done = False
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():  # and request.user.is_authenticated():
            options, question = create_question_from_form(category_id, form, request)
            question.save()
            for option in options:
                option.question = question
                option.save()
            done = True
        else:
            print "form is invalid"

    else:
        form = QuestionForm()

    context_data = {'form': form, "done": done, "category": Category.objects.get(id=category_id)}
    return render(request, 'add_question.html', context_data)


@login_required
def edit_question(request, category_id):
    done = False
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():  # and request.user.is_authenticated():
            options, question = create_question_from_form(category_id, form, request)

            question_from_db = Question.objects.filter(question=request.session['question_before_edit_id'])[0]
            question_from_db.question = question.question
            question_from_db.options = question.options
            question_from_db.creation_date = question.creation_date
            question_from_db.category = question.category
            question_from_db.creator = question.creator
            question_from_db.save()

            options_from_db = Option.objects.filter(question=question_from_db)
            for i in xrange(0, len(options)):
                option = options_from_db[i]
                option.is_correct = options[i].is_correct
                option.text = options[i].text
                option.question = question_from_db
                option.save()

            done = True
        else:
            print "form is invalid"

    else:
        form = QuestionForm()

    context_data = {'form': form, "done": done, 'showing_id':int(category_id), "category": Category.objects.get(id=category_id)}
    return render(request, 'edit_question.html', context_data)
