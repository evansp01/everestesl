from django.shortcuts import render, get_object_or_404
# Decorator to use built-in authentication system
from django.http import Http404

# Used to create and manually log in a user

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from everest.forms import *
from django.contrib.auth.decorators import login_required


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
    return render(request, 'everest/lesson/create_lesson.html', context)


@login_required
@transaction.atomic
def edit_lesson(request, lesson):  # TODO: actually use permissions
    lesson = get_object_or_404(Lesson, id=lesson)
    context = {'lesson': lesson}
    if request.user != lesson.creator:
        raise Http404("Access denied")
    if request.method == 'POST':
        form = AddSentence(request.POST)
        if form.is_valid():
            new_sentence = Sentence(english=form.cleaned_data['sentence'], creator=request.user)
            new_sentence.save()
            lesson.sentences.add(new_sentence)
            lesson.save()
        elif form.is_bound:
            context['errors'] = form.errors
    return render(request, 'everest/lesson/edit_lesson.html', context)

@login_required
@transaction.atomic
def add_sentence(request, sentence, lesson):
    sentence = get_object_or_404(Sentence, id=sentence)
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.user != lesson.creator:
        raise Http404("Access denied")
    else:
        lesson.sentences.add(sentence)
        lesson.save()
        return render(request, 'everest/lesson/edit_lesson.html', {'lesson': lesson})
    return render(request, 'everest/sentence/sentence.html', {'sentence': sentence})
