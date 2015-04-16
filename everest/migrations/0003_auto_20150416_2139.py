# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import everest.models


class Migration(migrations.Migration):

    dependencies = [
        ('everest', '0002_auto_20150416_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='englishaudio',
            name='audio',
            field=models.FileField(upload_to=everest.models.english_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nepaliaudio',
            name='audio',
            field=models.FileField(upload_to=everest.models.nepali_path),
            preserve_default=True,
        ),
    ]
