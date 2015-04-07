from django.db import models
import os

# User class for built-in authentication module
from django.contrib.auth.models import User


class Sentence(models.Model):
    english = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    def __unicode__(self):
        return self.english

class UserProfile(models.Model):
    userkey = models.OneToOneField(User)
    bio = models.CharField(max_length=430, blank=True)
    image = models.ImageField(upload_to="pictures", blank=True, null=True)
    ESLTEACHER = 'E'
    TRANSLATOR = 'T'
    USER_TYPES = (
        (ESLTEACHER, 'ESL_Teacher'),
        (TRANSLATOR, 'Translator'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPES)

class Lesson(models.Model):
    title = models.CharField(max_length=50)
    sentences = models.ManyToManyField(Sentence, related_name='lessons', symmetrical=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    def __unicode__(self):
        return self.title
    # link to mp3

class NepaliAudio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence, related_name='nep_audio')
    audio = models.FileField(upload_to='nepali')
    #filefiled

class EnglishAudio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence, related_name='eng_audio')
    audio = models.FileField(upload_to='english')

class Translation(models.Model):
    nepali = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='translations')
    sentence = models.ForeignKey(Sentence, related_name='translations')
    def __unicode__(self):
        return self.nepali

