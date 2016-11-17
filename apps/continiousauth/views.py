from django.shortcuts import render

from .serializers import AuthenticationSessionSerializer
from .models import AuthenticationSession

from rest_framework import generics


class AuthenticationSessionList(generics.ListAPIView):
    queryset = AuthenticationSession.objects.all()
    serializer_class = AuthenticationSessionSerializer


class CreateAuthenticationSession(generics.CreateAPIView):
    queryset = AuthenticationSession.objects.all()
    serializer_class = AuthenticationSessionSerializer