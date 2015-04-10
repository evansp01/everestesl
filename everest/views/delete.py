from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
import urllib
import json
import mimetypes
from everest.models import *
from everest.forms import *

@login_required
@transaction.atomic
def del_translation(request, translation):
    translation = get_object_or_404(Translation, id=translation)
    context = {'sentence': translation.sentence}
    if request.method == 'POST' and request.user == translation.creator:
        translation.delete()
    return render(request, 'everest/sentence.html', context)
