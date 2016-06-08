from django.conf.urls import patterns, url

urlpatterns = patterns('apps.authentication.views',
        url(r'^login/$', 'login', name='auth_login'),
        url(r'^logout/$', 'logout', name='auth_logout')
)
