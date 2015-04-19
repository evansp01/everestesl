# Decorator to use built-in authentication system

# Used to create and manually log in a user

# Django transaction system so we can use @transaction.atomic
from django.shortcuts import render

from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json

from everest.forms import *


@login_required
def manage_account(request):
    return render(request, 'everest/profile/edit_profile.html', {})
    # context = {}
    # if request.method == 'GET':    # GET request: display form
    # context['form'] = ProfileForm()


    # form = ProfileForm(request.POST.copy())
    #
    # if not form.is_valid():      # if form invalid, redisplay
    #     context['form'] = form
    #     return render(request, 'everest/profile/edit_profile.html', context)
    #
    # else:    # valid form; make requested changes
    #     request.user.first_name=form.cleaned_data['first_name']
    #     request.user.last_name=form.cleaned_data['last_name']
    #     request.user.email=form.cleaned_data['email']
    #     request.user.profile.bio=form.cleaned_data['bio']
    # #    request.user.profile.user_type =form.cleaned_data['user_type']
    #     request.user.save()
    #     request.user.profile.save()
    #     context['profile'] = request.user.profile
    #     return render(request, 'everest/profile/profile.html', context)


@login_required
@transaction.atomic
def change_personal(request):
    if not request.POST:
        return Http404("Get not available")
    form = ChangePersonalForm(request.POST.copy())
    if form.is_valid():
        pass
    return render(request, 'everest/profile/edit_personal_form.html', {})


@login_required
@transaction.atomic
def change_picture(request):
    print request
    print request.POST
    print request.FILES
    if not request.POST:
        return Http404("Get not available")
    form = ChangePictureForm(request.POST.copy(), request.FILES)
    if form.is_valid():
        request.user.profile.image = form.cleaned_data['image']
        request.user.profile.save()
    response = {}
    if request.user.profile.image:
        response['image'] = request.user.profile.image.url
    else:
        response['image'] = ''
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required
@transaction.atomic
def change_password(request):
    if not request.POST:
        return Http404("Get not available")
    form = ChangePasswordForm(request.POST.copy())
    if form.is_valid():
        pass
    return render(request, 'everest/profile/edit_password_form.html', {})
