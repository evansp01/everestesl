import uuid

from django.db import models


# User class for built-in authentication module
from django.contrib.auth.models import User


class Sentence(models.Model):
    english = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.english

def picture_path(instance, filename):
    return 'userpic/{0}{1}{2}'.format(instance.username, uuid.uuid4(), filename)

class UserProfile(models.Model):
    userkey = models.OneToOneField(User, related_name='profile')
    bio = models.CharField(max_length=430, blank=True)
    image = models.ImageField(upload_to="pictures", blank=True, null=True)
    ESLTEACHER = 'E'
    TRANSLATOR = 'T'
    OTHER = 'O'
    USER_TYPES = (
        (ESLTEACHER, 'ESL_Teacher'),
        (TRANSLATOR, 'Translator'),
        (OTHER, 'Other')
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPES)


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    sentences = models.ManyToManyField(Sentence, related_name='lessons', symmetrical=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='lessons')

    def __unicode__(self):
        return self.title
        # link to mp3


def nepali_path(instance, filename):
    return 'nepali/{0}{1}'.format(uuid.uuid4(), filename)


def english_path(instance, filename):
    return 'english/{0}{1}'.format(uuid.uuid4(), filename)


class NepaliAudio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence, related_name='nep_audio')
    audio = models.FileField(upload_to=nepali_path)
    # filefiled


class EnglishAudio(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    sentence = models.ForeignKey(Sentence, related_name='eng_audio')
    audio = models.FileField(upload_to=english_path)


class Translation(models.Model):
    nepali = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='translations')
    sentence = models.ForeignKey(Sentence, related_name='translations')

    def __unicode__(self):
        return self.nepali

