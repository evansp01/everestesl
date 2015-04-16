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

def need_translation(request):
    sentences = Sentence.objects.filter(translations__isnull=True)
    return render(request, 'everest/general/list_of_sentences.html', {'sentences' : sentences})

def need_audio(request):
    sentences = Sentence.objects.filter(nep_audio__isnull=True)
    return render(request, 'everest/general/list_of_sentences.html', {'sentences' : sentences})

def profile(request):
    return render(request, 'everest/profile.html', {})
