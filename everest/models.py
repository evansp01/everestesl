from django.db import models
import os

# User class for built-in authentication module
from django.contrib.auth.models import User


class Sentence(models.Model):
    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    def __unicode__(self):
        return self.text

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

class List(models.Model):
    sentences = models.ManyToManyField(Sentence, related_name='lists', symmetrical=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)


class NepaliAudio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence)
    audio = models.FileField(upload_to='nepali')
    #filefiled

class EnglishAudio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence)
    audio = models.FileField(upload_to='english')


class Translation(models.Model):
    nepali = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence)

