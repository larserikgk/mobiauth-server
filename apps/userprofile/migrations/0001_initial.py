# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 11:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('require_biometrics_photo', models.BooleanField(default=False)),
                ('require_proctoring_audio', models.BooleanField(default=False)),
                ('require_proctoring_video', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_user_id', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.Organization'),
        ),
    ]
