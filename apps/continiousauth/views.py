from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..userprofile.models import Application
from .serializers import AuthenticationSessionSerializer
from .models import AuthenticationSession

from rest_framework import generics


class AuthenticationSessionList(generics.ListAPIView):
    queryset = AuthenticationSession.objects.all()
    serializer_class = AuthenticationSessionSerializer


class CreateAuthenticationSession(generics.CreateAPIView):
    queryset = AuthenticationSession.objects.all()
    serializer_class = AuthenticationSessionSerializer


@api_view(['GET'])
def verify_authentication_session(request, external_session_id):
    user = request.user
    response = Response()

    if not user.is_authenticated():
        response.status_code = 403
        return response

    if not AuthenticationSession.objects.filter(external_session_id=external_session_id).exists():
        response.status_code = 404
        return response

    authentication_session = AuthenticationSession.objects.get(external_session_id=external_session_id)
    application = authentication_session.application

    if not application.has_access(user, application.get_user_uri()):
        response.status_code = 403
        return response

    if authentication_session.flag == 2 or authentication_session.flag == 3:
        response.status_code = 429

    authentication_session.flag = 2
    authentication_session.save()
    response.status_code = 200

    return response
