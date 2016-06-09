from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import *


def index(request):
    if request.user.is_authenticated():
        template = loader.get_template('userprofile/index_authenticated.html')
    else:
        template = loader.get_template('userprofile/index.html')
    user_profiles = UserProfile.objects.filter(user=request.user)
    organizations = []
    applications = []
    for profile in user_profiles:
        organizations.append(profile.organization)
    for application in Application.objects.all():
        if application.has_access(request.user, application.get_user_uri()):
            applications.append(application)

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
    profile = None
    if UserProfile.objects.filter(organization=org, user=request.user).exists():
        profile = UserProfile.objects.get(organization=org, user=request.user)
    else:
        org = None

    context = {
        'organization': org,
        'profile': profile
    }
    return HttpResponse(template.render(context, request))
