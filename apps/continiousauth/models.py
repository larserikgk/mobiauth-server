from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from ..userprofile.models import Application

FLAGS = ((1, 'Undetermined'), (2, 'Accepted'), (3, 'Declined'))


class AuthenticationSession(models.Model):
    application = models.ForeignKey(Application)
    external_session_id = models.UUIDField(blank=True, null=True)
    session_photo_bytes = models.TextField(blank=True, null=True)
    flag = models.SmallIntegerField('Flag', choices=FLAGS, default=1, blank=True)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.pk)
