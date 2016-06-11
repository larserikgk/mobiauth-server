from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import *


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
