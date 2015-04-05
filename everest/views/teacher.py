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
def edit_lesson(request):
    errors = []
    if request.method == 'POST':
        form = AddSentence(request.POST)

        if form.is_valid():
            new_sentence = Sentence(text=form.cleaned_data['sentence'], user=request.user)
            new_post.save()
        elif form.is_bound:
            for field, error in form.errors.iteritems():
                errors.append((field, error))

    sentences = Sentence.objects.all()
    context = {'sentences' : sentences, 'errors' : errors}
    return render(request, 'everest/edit_lesson.html', context)


def user_lessons(request):
    return render(request, 'everest/list_of_lessons.html', {})

def profile(request):
    return render(request, 'everest/profile.html', {})
