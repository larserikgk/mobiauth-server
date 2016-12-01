from django.conf.urls import url, include
from django.contrib import admin
from . import settings
from apps.userprofile.views import api_root, OrganizationList, OrganizationDetail, ApplicationList, ApplicationDetail,\
    UserProfileList, UserList, UserDetail
from apps.continiousauth.views import AuthenticationSessionList, CreateAuthenticationSession,\
    verify_authentication_session

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
    url(r'^authentication/create', CreateAuthenticationSession.as_view(), name='create_authentication_session'),
    url(r'^authentication/verify/(?P<external_session_id>.+)/$',
        verify_authentication_session,
        name='verify_authentication_session')
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
