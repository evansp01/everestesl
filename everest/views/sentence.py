from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
import json
from everest.models import *
from everest.forms import *

def view_sentence(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)

def record_english(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence, 'language':'english'}
    return render(request, 'everest/record.html', context)

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

def upload_audio(request, sentence):
    print request.POST
    print request.FILES
    print request.GET
    #print request
    if request.POST:
        #print request.POST
        #print blob
        #print request.FILES
        pass
    to_json = {'yes': "hi"}
    return HttpResponse(json.dumps(to_json), content_type='application/json')



