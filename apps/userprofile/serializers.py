from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Organization, UserProfile, Application


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'organization', 'external_user_id', 'image')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name', 'organization', 'require_biometrics_photo', 'require_proctoring_audio',
                  'require_proctoring_video', 'authentication_url_success', 'authentication_url_failure')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
