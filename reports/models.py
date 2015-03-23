from django.db import models
import os

# User class for built-in authentication module
from django.contrib.auth.models import User


class Sentence(models.Model):
    english = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    def __unicode__(self):
        return self.text

class UserProfile(models.Model):
    userkey = models.OneToOneField(User)
    age = models.PositiveIntegerField(null=True)
    bio = models.CharField(max_length=430, blank=True)
    image = models.ImageField(upload_to="pictures", blank=True)

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

