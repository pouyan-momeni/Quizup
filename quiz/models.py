from __future__ import unicode_literals

from django.db import models
from questions.models import Category, Question
from django.contrib.auth.models import User
import random
# from registration import models


class Quiz(models.Model):
    # badge = models.IntegerField(random.random()*10000)
    category = models.ForeignKey(Category)
    user1 = models.ForeignKey(User, related_name="user1", blank = True, null=True)
    user2 = models.ForeignKey(User, related_name="user2", blank = True, null=True)
    user1Score = models.IntegerField(default=None, blank = True, null=True)
    user2Score = models.IntegerField(default=None, blank = True, null=True)
    questions = models.ManyToManyField(Question)

    def get_user1(self):
        return self.user1

    def get_user2(self):
        return self.user2

    def set_user1(self, _user1):
        self.user1 = _user1

    def set_user2(self, _user2):
        self.user2 = _user2

    def set_user1Score(self, _user1Score):
        self.user1Score = _user1Score

    def set_user2Score(self, _user2Score):
        self.user2Score = _user2Score

    def set_category(self, _category):
        self.category = _category

    def add_question(self, question):
        self.questions.add(question)


# class SelectedQuestion(models.Model):
#     question = models.ForeignKey(Question)
#     quiz = models.ForeignKey(Quiz)

