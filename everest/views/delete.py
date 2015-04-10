from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
import urllib
import json
import mimetypes
from everest.models import *
from everest.forms import *

@login_required
@transaction.atomic
def del_translation(request, translation):
    translation = get_object_or_404(Translation, id=translation)
    sentence = translation.sentence
    if request.method == 'POST' and request.user == translation.creator:
        translation.delete()
        cleanup(sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)

@login_required
@transaction.atomic
def del_englishaudio(request, audio):
    audio = get_object_or_404(EnglishAudio, id=audio)
    sentence = audio.sentence
    if request.method == 'POST' and request.user == audio.creator:
        audio.delete()
        cleanup(sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)

@login_required
@transaction.atomic
def del_nepaliaudio(request, audio):
    audio = get_object_or_404(NepaliAudio, id=audio)
    sentence = audio.sentence
    if request.method == 'POST' and request.user == audio.creator:
        audio.delete()
        cleanup(sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)

@login_required
@transaction.atomic
def del_sentence(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    if request.method == 'POST' and request.user == sentence.creator:
        # figure out which lesson this is. Delete sentence from its sentences. Put lesson in context
        cleanup(sentence)
    return render(request, 'everest/lesson.html', context)

@login_required
@transaction.atomic
def del_lesson(request, lesson):
    context = {'lesson': lesson}
    # cleanup all sentences in it
    return render(request, 'everest/sentence.html', context)

def cleanup(sentence):
    #todo
    return
