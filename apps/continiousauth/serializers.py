from rest_framework import serializers

from .models import AuthenticationSession


class AuthenticationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationSession
        fields = ('application', 'external_session_id', 'session_photo_bytes', 'flag')
