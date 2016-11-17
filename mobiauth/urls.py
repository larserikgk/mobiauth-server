"""mobiauth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import settings
from apps.userprofile.views import api_root, OrganizationList, OrganizationDetail, ApplicationList, ApplicationDetail,\
    UserProfileList, UserList, UserDetail
from apps.continiousauth.views import AuthenticationSessionList,  CreateAuthenticationSession

api_urls = [
    # Root
    url(r'^$', api_root),
    # Organizations
    url(r'^organizations/$', OrganizationList.as_view(), name='organization_list'),
    url(r'^organizations/(?P<pk>[0-9]+)$', OrganizationDetail.as_view()),
    # Applications
    url(r'^applications/$', ApplicationList.as_view(), name='application_list'),
    url(r'^applications/(?P<pk>[0-9]+)$', ApplicationDetail.as_view()),
    # Users
    url(r'^userprofiles/$', UserProfileList.as_view(), name='userprofile_list'),
    url(r'^users/$', UserList.as_view(), name='user_list'),
    url(r'^users/(?P<username>.+)/$', UserDetail.as_view(), name='user_detail'),
    # Continuous authentication
    url(r'^authentication/$', AuthenticationSessionList.as_view(), name='authentication_session_list'),
    url(r'^authentication/create', CreateAuthenticationSession.as_view(), name='create_authentication_session')
]

urlpatterns = [
    # App urls
    url(r'^', include('apps.userprofile.urls')),
    url(r'^auth/', include('apps.authentication.urls')),
    # Administration urls
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Api urls
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(api_urls)),

]
