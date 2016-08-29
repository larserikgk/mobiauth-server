from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def organization_list(request, format=None):
    """
    List all organizations, or create a new organization.
    """
    if request.method == 'GET':
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def organization_detail(request, pk, format=None):
    """
    Retrieve, update or delete a organization instance.
    """
    try:
        organization = Organization.objects.get(pk=pk)
    except Organization.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def application_list(request, format=None):
    """
    List all applications, or create a new application.
    """
    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def application_detail(request, pk, format=None):
    """
    Retrieve, update or delete a application instance.
    """
    try:
        application = Application.objects.get(pk=pk)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
