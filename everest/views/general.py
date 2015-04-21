from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.tokens import default_token_generator

from django.db import transaction
from everest.forms import *


def home(request):
    return render(request, 'everest/index.html', {})


def view_lesson(request, lesson):
    lesson = get_object_or_404(Lesson, id=lesson)
    context = {'lesson': lesson}
    return render(request, 'everest/lesson/lesson.html', context)


@login_required
def view_self(request):
    return redirect('view_user', username=request.user.username)


def view_user(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    context = {'profile': profile}
    if profile.user_type == "E":
        context["lessons"] = profile.userkey.lessons.all
        context["sentences"] = None
    elif profile.user_type == "T":
        context["lessons"] = None
        s = set([translation.sentence for translation in user.translations.all()])
        s = s.union(set([recording.sentence for recording in user.nep_recordings.all()]))
        context["sentences"] = s
    return render(request, 'everest/profile/profile.html', context)


@transaction.atomic
def register(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'everest/signin_register/register.html', context)
    form = RegisterForm(request.POST.copy())
    if not form.is_valid():
        form.data['password'] = None
        form.data['password2'] = None
        context['form'] = form
        return render(request, 'everest/signin_register/register.html', context)
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
    new_user.is_active = False
    new_user.save()
    profile = UserProfile.objects.create(
        userkey=new_user,
        bio='',
        user_type=form.cleaned_data['user_type'],
    )
    profile.save()

    token = default_token_generator.make_token(new_user)
    url = request.get_host() + reverse('confirm_account', args=(new_user.username, token))
    context = {'user': new_user, 'url': url}
    email_html = render_to_string('email/register.txt', context)
    email_text = render_to_string('email/register.html', context)

    send_mail(subject="Verify your email address",
              html_message=email_html,
              message=email_text,
              from_email="everesteslwebmaster@gmail.com",
              recipient_list=[new_user.email])
    return render(request, 'everest/signin_register/confirm_sent.html', context)


@transaction.atomic
def confirm(request, username, token):
    user = get_object_or_404(User, username=username)
    if not user.is_active:
        if not default_token_generator.check_token(user, token):
            raise Http404("Incorrect token")
        user.is_active = True
        user.save()
    return render(request, 'everest/signin_register/account_confirmed.html', {'user': user})


def reset_form(request):
    context = {}
    if request.POST:
        form = ResetForm(request.POST)
        if form.is_valid():
            users = User.objects.filter(username=form.cleaned_data['username'])
            if users.all():
                send_reset_email(request, users[0])
                context['requestor'] = users[0]
                return render(request, 'everest/signin_register/reset_sent.html', context)
            else:
                context['error'] = 'Username does not exist'
        else:
            context['form'] = form
    return render(request, 'everest/signin_register/reset_request.html', context)


def send_reset_email(request, user):
    token = default_token_generator.make_token(user)
    url = request.get_host() + reverse('reset_password', args=(user.username, token))
    context = {'user': user, 'url': url}
    email_html = render_to_string('email/reset.txt', context)
    email_text = render_to_string('email/reset.html', context)

    send_mail(subject="Information regarding your Everest account",
              html_message=email_html,
              message=email_text,
              from_email="everesteslwebmaster@gmail.com",
              recipient_list=[user.email])


@transaction.atomic
def reset_password(request, username, token):
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, token):
        raise Http404("Incorrect token")
    random_pass = User.objects.make_random_password()
    send_password_email(user, random_pass)
    user.set_password(random_pass)
    user.save()
    return render(request, 'everest/signin_register/password_sent.html', {'requestor': user})


def send_password_email(user, password):
    context = {'user': user, 'password': password}
    email_html = render_to_string('email/password.txt', context)
    email_text = render_to_string('email/password.html', context)

    send_mail(subject="Information regarding your Everest account",
              html_message=email_html,
              message=email_text,
              from_email="everesteslwebmaster@gmail.com",
              recipient_list=[user.email])
