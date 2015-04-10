# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('audio', models.FileField(upload_to=b'english')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NepaliAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('audio', models.FileField(upload_to=b'nepali')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('english', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nepali', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(related_name='translations', to=settings.AUTH_USER_MODEL)),
                ('sentence', models.ForeignKey(related_name='translations', to='everest.Sentence')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.CharField(max_length=430, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'pictures', blank=True)),
                ('user_type', models.CharField(max_length=1, choices=[(b'E', b'ESL_Teacher'), (b'T', b'Translator')])),
                ('userkey', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nepaliaudio',
            name='sentence',
            field=models.ForeignKey(related_name='nep_audio', to='everest.Sentence'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='sentences',
            field=models.ManyToManyField(related_name='lessons', to='everest.Sentence', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='englishaudio',
            name='sentence',
            field=models.ForeignKey(related_name='eng_audio', to='everest.Sentence'),
            preserve_default=True,
        ),
    ]
