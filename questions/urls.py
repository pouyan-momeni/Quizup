from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^categories/$', views.show_categories, name='show_categories'),
    url(r'^category/(?P<category_id>[0-9]+)$', views.show_category, name='show_category'),
    url(r'^(?P<question_id>[0-9]+)/$', views.view_question, name='view_question'),
    url(r'^add_category/$', views.create_a_category, name='add_category'),
    url(r'^add_question/(?P<category_id>[0-9]+)$', views.create_a_question, name='add_question'),
    url(r'^edit_question/(?P<category_id>[0-9]+)$', views.edit_question, name='edit_question'),
    url(r'^ranking/(?P<category_id>[0-9]*)$', views.show_ranking, name='show_ranking'),
    ]
