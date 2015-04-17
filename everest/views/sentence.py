from subprocess import Popen, PIPE
import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.files.base import ContentFile
from django.conf import settings
import os

from everest.forms import *


FFMPEG_PATH = settings.FFMPEG_INSTALL + 'ffmpeg'
SERVER_SIDE_ENCODING = 'mp3'


def view_sentence(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)


@login_required
def record_english(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence, 'language': 'english'}
    return render(request, 'everest/record.html', context)


@login_required
def record_nepali(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence, 'language': 'nepali'}
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
        print type(form.cleaned_data['audio'])
        audio_file = file_to_mp3(form.cleaned_data['audio'])
        if form.cleaned_data['language'] == 'english':
            audio = EnglishAudio(creator=request.user,
                                 sentence=sentence)
            audio.audio.save('audio.' + SERVER_SIDE_ENCODING, audio_file)
            audio.save()
        elif form.cleaned_data['language'] == 'nepali':
            audio = NepaliAudio(creator=request.user,
                                sentence=sentence)
            audio.audio.save('audio.' + SERVER_SIDE_ENCODING, audio_file)
            audio.save()
        else:
            raise Http404("langauge parameter not understood")
        return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
    print form.errors
    raise Http404("Form data failed to validate")


# subprocess call to ffmpeg
def file_to_mp3(infile):
    args = [FFMPEG_PATH, '-i', '-', '-f', SERVER_SIDE_ENCODING, '-']
    with open(os.devnull, 'wb') as devnull:
        ffmpeg_proc = Popen(args, stdout=PIPE, stdin=PIPE, stderr=devnull)
    output = ffmpeg_proc.communicate(infile.read())
    return ContentFile(output[0])


def english_audio(request, audio):
    audio = get_object_or_404(EnglishAudio, id=audio)
    return HttpResponse(audio.audio, content_type='audio/' + SERVER_SIDE_ENCODING)


def nepali_audio(request, audio):
    audio = get_object_or_404(NepaliAudio, id=audio)
    return HttpResponse(audio.audio, content_type='audio/' + SERVER_SIDE_ENCODING)