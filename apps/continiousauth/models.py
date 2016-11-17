from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from ..userprofile.models import Application, UserProfile

FLAGS = ((1, 'Undetermined'), (2, 'Accepted'), (3, 'Declined'))


class AuthenticationSession(models.Model):
    application = models.ForeignKey(Application)
    user_profile = models.ForeignKey(UserProfile)
    flag = models.SmallIntegerField('Flag', choices=FLAGS, default=1, blank=True)
    start_time = models.TimeField(default=datetime.now())
    end_time = models.TimeField(blank=True, null=True)

    def __unicode__(self):
        return self.pk
