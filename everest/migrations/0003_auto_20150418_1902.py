# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('everest', '0002_auto_20150418_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(max_length=1, choices=[(b'E', b'ESL_Teacher'), (b'T', b'Translator'), (b'O', b'Other')]),
            preserve_default=True,
        ),
    ]
