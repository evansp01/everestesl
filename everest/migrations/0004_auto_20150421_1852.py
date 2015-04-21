# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('everest', '0003_auto_20150418_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishaudio',
            name='creator',
            field=models.ForeignKey(related_name='eng_recordings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='nepaliaudio',
            name='creator',
            field=models.ForeignKey(related_name='nep_recordings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='english',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(max_length=1, choices=[(b'E', b'ESL teacher'), (b'T', b'Translator'), (b'O', b'Other')]),
        ),
    ]
