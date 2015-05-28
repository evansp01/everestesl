from haystack import indexes

import everest.models as models
from django.contrib.auth.models import User


class LessonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator')
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return models.Lesson

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SentenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='creator')
    created = indexes.DateTimeField(model_attr='created')

    def get_model(self):
        return models.Sentence

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    creator = indexes.CharField(model_attr='date_joined')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
