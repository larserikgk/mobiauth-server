from django.contrib import admin
from . models import UserProfile, Organization, Application

admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(Application)
