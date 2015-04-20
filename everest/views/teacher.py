from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from django.db import transaction
from django.contrib.auth.decorators import login_required

from everest.forms import *


@login_required
@transaction.atomic
def create_lesson(request):
    context = {}
    if request.method == 'POST':
        form = AddLesson(request.POST)
        if form.is_valid():
            new_lesson = Lesson(title=form.cleaned_data['title'], creator=request.user)
            new_lesson.save()
            return redirect(reverse('edit_lesson', kwargs={'lesson': new_lesson.id}))
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
        else:
            context['errors'] = form.errors
    return render(request, 'everest/lesson/edit_lesson.html', context)


@login_required
@transaction.atomic
def add_sentence(request, sentence, lesson):
    sentence = get_object_or_404(Sentence, id=sentence)
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.user != lesson.creator:
        raise Http404("Access denied")
    lesson.sentences.add(sentence)
    lesson.save()
    return render(request, 'everest/lesson/edit_lesson.html', {'lesson': lesson})
