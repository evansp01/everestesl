from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from everest.forms import *


def home(request):
    return render(request, 'everest/index.html', {})


def all_lessons(request):
    context = {'lessons': Lesson.objects.all()}
    return render(request, 'everest/general/list_of_lessons.html', context)


def all_sentences(request):
    context = {'sentences': Sentence.objects.all()}
    return render(request, 'everest/general/list_of_sentences.html', context)


def all_users(request):
    context = {'users': User.objects.all()}
    return render(request, 'everest/general/list_of_users.html', context)


def find_lesson(request, userid=None):
    if not userid:
        userid = request.user.id
    user = get_object_or_404(User, id=userid)
    context = {'lessons': user.lessons.all()}
    return render(request, 'everest/general/list_of_lessons.html', context)


@login_required
def find_my_lessons(request):
    return redirect('find_lesson', userid=request.user.id)


def find_sentence(request, userid):
    context = {'sentences': userid.sentences.all()}
    return render(request, 'everest/general/list_of_sentences.html', context)


# def find_user(request, userid):
# context = {'users' :
# return render(request, 'everest/general/list_of_users.html', context)

def view_lesson(request, lesson):
    lesson = get_object_or_404(Lesson, id=lesson)
    context = {'lesson': lesson}
    return render(request, 'everest/lesson.html', context)

def view_user(request, username):
    user = get_object_or_404(User, username=username)
    context = {'profile': user.profile}
    return render(request, 'everest/profile.html', context)

@login_required
@transaction.atomic
def manage_account(request):
    context = {}
    if request.method == 'GET':    # GET request: display form
        context['form'] = ProfileForm()
        return render(request, 'everest/account.html', context)

    form = ProfileForm(request.POST.copy())
    
    if not form.is_valid():      # if form invalid, redisplay
        context['form'] = form
        return render(request, 'everest/account.html', context)
    
    else:    # valid form; make requested changes
        request.user.first_name=form.cleaned_data['first_name']
        request.user.last_name=form.cleaned_data['last_name']
        request.user.email=form.cleaned_data['email']
        request.user.profile.bio=form.cleaned_data['bio']
    #    request.user.profile.user_type =form.cleaned_data['user_type']
        request.user.save()
        request.user.profile.save()
        context['profile'] = request.user.profile
        return render(request, 'everest/profile.html', context)
    
        

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
    # everything is okay, register
    username = form.cleaned_data['username']
    password = form.cleaned_data['password1']
    new_user = User.objects.create_user(
        username=username,
        password=password,
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email=form.cleaned_data['email'],
    )
    # new_user.is_active = False
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
