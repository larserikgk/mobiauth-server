from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import *
from .permissions import HasApplicationAdminAccess, AuthenticatedUserEqualsQueriedUser
from .serializers import *
from rest_framework import generics
from rest_framework import permissions


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'organizations': reverse('organization_list', request=request, format=format),
        'applications': reverse('application_list', request=request, format=format),
        'userprofiles': reverse('userprofile_list', request=request, format=format),
        'users': reverse('user_list', request=request, format=format),
    })


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class ApplicationList(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, HasApplicationAdminAccess)
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, AuthenticatedUserEqualsQueriedUser)
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])


def index(request):
    organizations = []
    applications = []
    if request.user.is_authenticated():
        template = loader.get_template('userprofile/index_authenticated.html')
        user_profiles = UserProfile.objects.filter(user=request.user)
        for profile in user_profiles:
            organizations.append(profile.organization)
        for application in Application.objects.all():
            if (application.has_access(request.user, application.get_user_uri()) or
                    application.has_access(request.user, application.get_admin_uri())):
                applications.append(application)
    else:
        template = loader.get_template('userprofile/index.html')

    context = {
        'user': request.user,
        'organizations': organizations,
        'applications': applications,
    }
    return HttpResponse(template.render(context, request))


def application(request, application_id):
    template = loader.get_template('userprofile/application.html')
    app = get_object_or_404(Application, id=application_id)
    if not app.has_access(request.user, app.get_user_uri()):
        app = None

    context = {'application': app}
    return HttpResponse(template.render(context, request))


def organization(request, organization_id):
    template = loader.get_template('userprofile/organization.html')
    org = get_object_or_404(Organization, id=organization_id)
    applications = Application.objects.filter(organization=org)
    application_user = []
    application_admin = []
    profile = None
    if UserProfile.objects.filter(organization=org, user=request.user).exists():
        profile = UserProfile.objects.get(organization=org, user=request.user)
    else:
        org = None

    context = {
        'organization': org,
        'profile': profile,
        'applications': applications,
    }
    return HttpResponse(template.render(context, request))
