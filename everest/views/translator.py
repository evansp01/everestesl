from django.shortcuts import render

from everest.forms import *


def home(request):
    return render(request, 'everest/index.html', {})


def need_translation(request):
    sentences = Sentence.objects.filter(translations__isnull=True)
    return render(request, 'everest/general/list_of_sentences.html', {'sentences': sentences})


def need_audio(request):
    sentences = Sentence.objects.filter(nep_audio__isnull=True)
    return render(request, 'everest/general/list_of_sentences.html', {'sentences': sentences})
