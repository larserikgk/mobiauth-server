from rest_framework import serializers

from .models import AuthenticationSession


class AuthenticationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationSession
        fields = ('application', 'user_profile', 'flag', 'start_time', 'end_time')
