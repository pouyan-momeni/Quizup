from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^index', views.index, name='index'),
    #url(r'^sign-in', views.sign_in, name='sign_in'),
    #url(r'^sign-up', views.sign_up, name='sign_up'),
    #url(r'^forgot-password', views.forgot_password, name='forgot_password'),
    #url(r'^accounts/register/$', views.registration_form, name='registration_form'),
]