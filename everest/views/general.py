from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'everest/index.html', {})



def find_list(request):
    return render(request, 'everest/index.html', {})

def find_user(request):
    return render(request, 'everest/index.html', {})

def find_sentence(request):
    return render(request, 'everest/index.html', {})

def manage_account(request):
    return render(request, 'everest/index.html', {})



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

@transaction.atomic
def register(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'everest/register.html', context)
    form = RegistrationForm(request.POST.copy())
    if not form.is_valid():
        form.data['password'] = None
        form.data['password2'] = None
        context['form'] = form
        return render(request, 'everest/register.html', context)
    #everything is okay, register
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    new_user = User.objects.create_user(
        username=username, 
        password=password,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'],
    )
#    new_user.is_active = False
    new_user.save()

    UserProfile.objects.create(
        userkey=new_user,
        bio='',
    )

    # Logs in the new user and redirects to main page
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
    login(request, new_user)
    return redirect('/everest/home')
