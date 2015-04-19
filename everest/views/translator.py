from django.shortcuts import render

from everest.forms import *


def home(request):
    return render(request, 'everest/index.html', {})


def need_translation(request):
    context = {'sentences': Sentence.objects.filter(translations__isnull=True)}
    context['head'] = "Sentences Needing Written Translation"
    return render(request, 'everest/lists/list_of_sentences.html', context)


def need_audio(request):
    context = {'sentences': Sentence.objects.filter(nep_audio__isnull=True)}
    context['head'] = "Sentences Needing Audio Translation"
    return render(request, 'everest/lists/list_of_sentences.html', context)