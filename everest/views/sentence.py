from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json
from everest.models import *


def home(request):
    return render(request, 'everest/record.html', {})

def upload(request):
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

def view_sentence(request, sentence):
    sentence = get_object_or_404(Sentence, id=sentence)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)

