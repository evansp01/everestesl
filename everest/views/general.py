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


def view_lesson(request, lesson):
    lesson = get_object_or_404(Lesson, id=lesson)
    context = {'lesson': lesson}
    return render(request, 'everest/lesson/lesson.html', context)


@login_required
def view_self(request):
    return redirect('view_user', username=request.user.username)


def view_user(request, username):
    user = get_object_or_404(User, username=username)
    context = {'profile': user.profile}
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
    # new_user.is_active = False
    new_user.save()
    profile = UserProfile.objects.create(
        userkey=new_user,
        bio='',
        user_type=form.cleaned_data['user_type'],
    )
    profile.save()


    # Logs in the new user and redirects to main page
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    login(request, new_user)
    return redirect(reverse('manage_account'))


# from django.core.mail import send_mail
# from django.template.loader import render_to_string
#
#
# msg_plain = render_to_string('templates/email.txt', {'some_params': some_params})
# msg_html = render_to_string('templates/email.html', {'some_params': some_params})
#
# send_mail(
#     'email title',
#     msg_plain,
#     'no-reply@example.com',
#     [some@reciver.com, ],
#     html_message=msg_html,
# )