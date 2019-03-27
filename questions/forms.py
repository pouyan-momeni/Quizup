# -*- coding: utf-8 -*-
from django import forms
from questions.models import Category


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=500, required=True, label=u"متن سوال")
    a = forms.CharField(max_length=500, required=True, label=u'الف')
    a_is_correct = forms.BooleanField(required=False, label='درست است؟')
    b = forms.CharField(max_length=500, required=True, label=u'ب')
    b_is_correct = forms.BooleanField(required=False, label='درست است؟')
    c = forms.CharField(max_length=500, required=True, label=u'پ')
    c_is_correct = forms.BooleanField(required=False, label='درست است؟')
    d = forms.CharField(max_length=500, required=True, label=u'ت')
    d_is_correct = forms.BooleanField(required=False, label='درست است؟')
#    categories = forms.ChoiceField(choices=Category.VISIBLE_CATEGORIES, required=True, label=u'دسته بندی')

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
#        all_categories = Category.objects.all()
#        for cat in all_categories:
#            self.fields['categories'].choices += [(cat.id, cat.name)]


my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value'
}


class AnsweredQuestionForm(forms.Form):
    a_is_selected = forms.BooleanField(required=False)
    b_is_selected = forms.BooleanField(required=False)
    c_is_selected = forms.BooleanField(required=False)
    d_is_selected = forms.BooleanField(required=False)


class CategoryForm(forms.Form):
    category_name = forms.CharField(max_length=80, required=True, label=u"نام دسته‌بندی", error_messages=my_default_errors)

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        cat_name = cleaned_data["category_name"]
        if len(Category.objects.filter(name=cat_name)) > 0:
            message = u"این نام قبلا استفاده شده‌است"
            self._errors["category_name"] = self.error_class([message])
            del cleaned_data["category_name"]

        return cleaned_data
