# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
import random


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    DEBUG_CATEGORIES = [(1, "Music"), (2, "Sport"), (3, "Computer Science")]
    VISIBLE_CATEGORIES = []

    def __unicode__(self):
        return unicode(self.name)

    def add_question(self, question): # TODO: no needed... hmmm?
        self.questions.append(question)

    def get_random_questions(self, number_of_questions):
        questions = Question.objects.filter(category=self)
        sample_value = min(len(questions), number_of_questions)
        print "sample value: " + str(sample_value)
        selected_question_numbers = random.sample(range(0, len(questions)), sample_value)
        result_questions = []
        for i in selected_question_numbers:
            result_questions.append(questions[selected_question_numbers[i]])
        return result_questions


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    category = models.ForeignKey(Category, default=None)
    score = models.BigIntegerField()


class Question(models.Model):
    question = models.CharField(max_length=500)
    options = models.CharField(max_length=500)
    creation_date = models.TimeField(auto_now=True)
    category = models.ForeignKey(Category)
    creator = models.ForeignKey(User)


class Option(models.Model):
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question)


