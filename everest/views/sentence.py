from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.db import transaction
import urllib
from django.contrib.auth.decorators import login_required
import json
import mimetypes
from everest.models import *
from everest.forms import *

def view_sentence(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)

@login_required
def record_english(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence, 'language':'english'}
    return render(request, 'everest/record.html', context)

@login_required
def record_nepali(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence, 'language':'nepali'}
    return render(request, 'everest/record.html', context)

@login_required
@transaction.atomic
def submit_translation(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence}
    if request.method == 'POST':
        form = NepaliTranslation(request.POST)
        if form.is_valid():
            translation = Translation(nepali=form.cleaned_data['translation'],
                                      creator=request.user,
                                      sentence=sentence)
            translation.save()
        else:
            context['errors'] = form.errors
    return render(request, 'everest/sentence.html', context)

@login_required
@transaction.atomic
def upload_audio(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    if request.method != 'POST':
        raise Http404("Method not supported on this url")
    form = AudioForm(request.POST, request.FILES)
    if form.is_valid():
        if form.cleaned_data['language'] == 'english':
            audio = EnglishAudio(audio=form.cleaned_data['audio'],
                                 creator=request.user,
                                 sentence=sentence)
            audio.save()
        elif form.cleaned_data['language'] == 'nepali':
            audio = NepaliAudio(audio=form.cleaned_data['audio'],
                                creator=request.user,
                                sentence=sentence)
            audio.save()
        else:
            raise Http404("langauge parameter not understood")
        return HttpResponse(json.dumps({"status":"success"}), content_type='application/json')
    print form.errors
    raise Http404("Form data failed to validate")


def english_audio(request, audio):
    audio = get_object_or_404(EnglishAudio, id=audio)
    url = urllib.pathname2url(audio.audio.name)
    content_type = mimetypes.guess_type(url)
    print content_type
    return HttpResponse(audio.audio, content_type='audio/wav')


def nepali_audio(request, audio):
    audio = get_object_or_404(NepaliAudio, id=audio)
    url = urllib.pathname2url(audio.audio.name)
    content_type = mimetypes.guess_type(url)
    return HttpResponse(audio.audio, content_type='audio/wav')
    






