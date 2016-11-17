from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'organization', (), {'organization_id': self.id}


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    external_user_id = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user.first_name + ' ' + self.user.last_name)


class Application(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization)
    require_biometrics_photo = models.BooleanField(default=False)
    require_proctoring_audio = models.BooleanField(default=False)
    require_proctoring_video = models.BooleanField(default=False)
    authentication_url_success = models.URLField(default='www.example.com/success')
    authentication_url_failure = models.URLField(default='www.example.com/failure')

    def save(self, *args, **kwargs):
        if not (Group.objects.filter(name=self.get_user_uri()).exists() or
                Group.objects.filter(name=self.get_admin_uri()).exists()):
            super(Application, self).save(*args, **kwargs)
            user_group = Group(name=self.get_user_uri())
            admin_group = Group(name=self.get_admin_uri())
            user_group.save()
            admin_group.save()
        else:
            super(Application, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user_group = Group.objects.get(name=self.get_user_uri())
        admin_group = Group.objects.get(name=self.get_admin_uri())
        user_group.delete()
        admin_group.delete()

    def add_user(self, user, name):
        user_group = Group.objects.get(name=name)
        user.groups.add(user_group)
        user.save()

    def remove_user(self, user, name):
        user_group = Group.objects.get(name=name)
        user.groups.remove(user_group)
        user.save()

    def get_user_uri(self):
        return 'App-' + self.name + '-User'

    def get_admin_uri(self):
        return 'App-' + self.name + '-Admin'

    def has_access(self, user, name):
        group = Group.objects.get(name=name)
        if group in user.groups.all():
            return True
        else:
            return False

    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return 'application', (), {'application_id': self.id}


