from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'application/(?P<application_id>\d+)', views.application, name='application'),
]