# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('everest', '0004_auto_20150420_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(max_length=1, choices=[(b'E', b'ESL teacher'), (b'T', b'Translator'), (b'O', b'Other')]),
            preserve_default=True,
        ),
    ]
