from django.shortcuts import render, redirect, get_object_or_404
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
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'everest/index.html', {})

@login_required
@transaction.atomic
def create_lesson(request):
    context = {}
    if request.method == 'POST':
        form = AddLesson(request.POST)
        if form.is_valid():
            new_lesson = Lesson(title=form.cleaned_data['title'], creator=request.user)
            new_lesson.save()
            return edit_lesson(request, new_lesson.id)
        else:
            context['errors'] = form.errors
    return render(request, 'everest/create_lesson.html', context)

@login_required
@transaction.atomic
def edit_lesson(request, lesson):    # TODO: actually use permissions
    lesson = get_object_or_404(Lesson, id=lesson)
    context = { 'lesson':lesson }
    if request.user != lesson.creator:
        raise Http404("Access denied")
    if request.method == 'POST':
        form = AddSentence(request.POST)
        if form.is_valid():
            new_sentence = Sentence(english=form.cleaned_data['sentence'], creator=request.user)
            new_sentence.save()
            lesson.sentences.add(new_sentence)
        elif form.is_bound:
            context['errors'] = form.errors
    return render(request, 'everest/edit_lesson.html', context)


def user_lessons(request):
    return render(request, 'everest/general/list_of_lessons.html', {})

def profile(request):
    return render(request, 'everest/profile.html', {})
