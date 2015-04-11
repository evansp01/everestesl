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
def del_sentence(request, sentence, lesson):
    sentence = get_object_or_404(Sentence, id=sentence)
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.method == 'POST' and request.user == lesson.creator:
        lesson.sentences.remove(sentence)
        cleanup(sentence)
    context = {'lesson': lesson}
    return render(request, 'everest/edit_lesson.html', context)

@login_required
@transaction.atomic
def del_lesson(request, lesson):
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.method == 'POST' and request.user == lesson.creator:
        if lesson.sentences.count():
            for sentence in lesson.sentences.all():
                cleanup(sentence)
    lesson.delete()
    context = {'lessons' : Lesson.objects.all()}
    return render(request, 'everest/general/list_of_lessons.html', context)

def cleanup(sentence):
    # if it has no translation AND no engaudio AND no nepaliaudio, delete it
    # should we check if it's in a lesson???
    #todo
    return
