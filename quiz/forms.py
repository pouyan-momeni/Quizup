# -*- coding: utf-8 -*-
from django import forms
from questions.models import Category
from questions.forms import CategoryForm


class QuizForm(forms.Form):
    categories = forms.ChoiceField(choices=Category.VISIBLE_CATEGORIES, required=True, label=u'دسته بندی')

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        all_categories = Category.objects.all()
        for cat in all_categories:
            self.fields['categories'].choices += [(cat.id, cat.name)]
