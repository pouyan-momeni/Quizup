from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start/$', views.start, name='start_quiz'),
    url(r'^end/$', views.end, name='end_quiz'),

    ]
