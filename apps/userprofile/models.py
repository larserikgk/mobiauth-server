from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    external_user_id = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True)

    def __unicode__(self):
        return self.user.email


class Application(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)
    require_biometrics_photo = models.BooleanField(default=False)
    require_proctoring_audio = models.BooleanField(default=False)
    require_proctoring_video = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name



