
from django.conf.urls import include, url
from django.contrib import admin
from questions import urls
from quiz import urls as quiz_urls
from django.contrib.auth.views import login
from django.contrib.auth.decorators import user_passes_test

login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), ('/questions/'), ('/quiz/'))

urlpatterns = [
    url(r'^accounts/login/$', login_forbidden(login), name="login"),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^questions/', include(urls)),
    url(r'^quiz/', include(quiz_urls)),
    url(r'^', include('user_management.urls')),

]

