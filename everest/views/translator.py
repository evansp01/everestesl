from django.shortcuts import render
#from django.shortcuts import render, redirect, get_object_or_404
#from django.core.exceptions import ObjectDoesNotExist
#from django.template.loader import render_to_string
#from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.defaults import page_not_found
import mimetypes
import urllib
from django.contrib.auth.tokens import default_token_generator

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from django.core.mail import send_mail
from everest.models import *
from everest.forms import *

def home(request):
    return render(request, 'everest/index.html', {})

#@login_required
#@transaction.atomic
def translate(request):  # check if translator? Must be logged in?
    errors = []
    context = {}
    snt = request.GET.get('s')   # ADD ERROR-CHECKING -- grab from submit button
    s = Sentence.objects.get(id=snt)
    if request.method == 'POST':
        form = AddTranslation(request.POST)
        if form.is_valid():
            new_translation = Translation(nepali=form.cleaned_data['translation'], creator=request.user, sentence=s)
            new_translation.save()
            
        elif form.is_bound:
            for field, error in form.errors.iteritems():
                errors.append((field, error))
            context['errors'] = errors
    context['sentence'] = s
    context['lessons'] = Lesson.objects.filter(sentences=s)
    context['translations'] = s.translation_set.all()
    return render(request, 'everest/sentence.html', context)


def need_translation(request):
    return render(request, 'everest/list_of_lessons.html', {})

def need_audio(request):
    return render(request, 'everest/list_of_lessons.html', {})

def profile(request):
    return render(request, 'everest/profile.html', {})
