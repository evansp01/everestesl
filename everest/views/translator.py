from django.shortcuts import render
# from django.shortcuts import render, redirect, get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
#from django.template.loader import render_to_string
#from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system

# Used to create and manually log in a user

# Django transaction system so we can use @transaction.atomic
from everest.forms import *


def home(request):
    return render(request, 'everest/index.html', {})


def need_translation(request):
    sentences = Sentence.objects.filter(translations__isnull=True)
    return render(request, 'everest/general/list_of_sentences.html', {'sentences': sentences})


def need_audio(request):
    sentences = Sentence.objects.filter(nep_audio__isnull=True)
    return render(request, 'everest/general/list_of_sentences.html', {'sentences': sentences})


def profile(request):
    return render(request, 'everest/profile.html', {})
