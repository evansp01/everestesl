from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
import json
from django.core.urlresolvers import reverse

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

def find_lesson(request):
    lessons = Lesson.objects.all()
    context = {'lessons' : lessons}
    return render(request, 'everest/list_of_lessons.html', context)

def find_user(request):
    return render(request, 'everest/list_of_users.html', {})

def find_sentence(request):
    context = {}
    context['sentences'] = Sentence.objects.all # for now, return all sentences
    return render(request, 'everest/list_of_sentences.html', context)

def view_lesson(request):
    errors = []
    comments = {}
    lsn = request.GET.get('l')   # ADD ERROR-CHECKING
    lesson = Lesson.objects.get(id=lsn)
    sentences = Sentence.objects.all # for now, return all sentences
    context = {'lesson' : lesson, 'sentences' : sentences}
    return render(request, 'everest/lesson.html', context)

def view_user(request):
    return render(request, 'everest/profile.html', {})

def view_sentence(request):
    return render(request, 'everest/sentence.html', {})

def manage_account(request):
    return render(request, 'everest/account.html', {})

def view_sentence(request):
    return render(request, 'everest/sentence.html', {})

@transaction.atomic
def register(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'everest/register.html', context)
    form = RegisterForm(request.POST.copy())
    if not form.is_valid():
        form.data['password'] = None
        form.data['password2'] = None
        context['form'] = form
        return render(request, 'everest/register.html', context)
    #everything is okay, register
    username = form.cleaned_data['username']
    password = form.cleaned_data['password1']
    new_user = User.objects.create_user(
        username=username,
        password=password,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'],
    )
    #new_user.is_active = False
    new_user.save()

    UserProfile.objects.create(
        userkey=new_user,
        bio='',
    )

    # Logs in the new user and redirects to main page
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect(reverse('home'))
