from django.shortcuts import render

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

# Create your views here.

def home(request):
    return render(request, 'everest/index.html', {})

#@login_required
#@transaction.atomic
def create_lesson(request):
    errors = []
    context = {}
    if request.method == 'POST':
        form = AddLesson(request.POST)

        if form.is_valid():
            new_lesson = Lesson(title=form.cleaned_data['title'], creator=request.user)
            new_lesson.save()
        elif form.is_bound: #QQQ: Can't this just be form.errors?
            for field, error in form.errors.iteritems():
                errors.append((field, error))
        context = {'this_lesson' : new_lesson, 'errors' : errors}
    return render(request, 'everest/create_lesson.html', context)

#@login_required
#@transaction.atomic
def edit_lesson(request):    # SHOULD ONLY BE POSSIBLE IF IT'S YOUR SENTENCE
    errors = []
    context = {}
    lsn = request.GET.get('l')
    lesson = Lesson.objects.get(id=lsn)
    if request.method == 'POST':
        form = AddSentence(request.POST)
        if form.is_valid():
            new_sentence = Sentence(english=form.cleaned_data['sentence'], creator=request.user)
            new_sentence.save()
            lesson.sentences.add(new_sentence)  # fix this to use the form data, not the URL

        elif form.is_bound:
            for field, error in form.errors.iteritems():
                errors.append((field, error))
            context['errors'] = errors
    context['lesson'] = lesson
    context['sentences'] = Sentence.objects.filter(lessons=lesson) # breaks if form breaks?
    return render(request, 'everest/edit_lesson.html', context)


def user_lessons(request):
    return render(request, 'everest/general/list_of_lessons.html', {})

def profile(request):
    return render(request, 'everest/profile.html', {})
