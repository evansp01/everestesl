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

@login_required
@transaction_atomic
def del_translation(request, translation):
    translation = get_object_or_404(Sentence, id=translation)
    context = {'sentence': translation.sentence}

#    if (request.user.id == translation.creator.id)
    translation.delete()

    return render(request, 'everest/sentence.html', context)


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
