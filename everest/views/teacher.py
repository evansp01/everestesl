from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required

from everest.forms import *
import os
from os.path import join
import uuid
import zipfile
import shutil



def zipdir(path, zipf):
    for root, dirs, files in os.walk(path):
        for f in files:
            zipf.write(os.path.join(root, f))


def download_lesson(request, lesson):
    lesson = get_object_or_404(Lesson, pk=lesson)
    tmp_dir = join('/tmp', str(uuid.uuid4()))
    os.mkdir(tmp_dir)
    lesson_dir = join(tmp_dir, 'lesson')
    os.mkdir(lesson_dir)
    for i, sentence in enumerate(lesson.sentences.all()):
        sent_dir = join(lesson_dir, 'sentence_{}'.format(i+1))
        os.mkdir(sent_dir)
        with open(join(sent_dir, 'english.txt'), "w") as english:
            english.write(sentence.english)
        for j, translation in enumerate(sentence.translations.all()):
            with open(join(sent_dir, 'translation_{}.txt'.format(j+1)), "w") as trans:
                trans.write(translation.nepali)
        for j, audio in enumerate(sentence.eng_audio.all()):
            with open(join(sent_dir, 'translation_{}.mp3'.format(j+1)), "wb") as eng:
                eng.write(audio.audio.file.read())
        for j, audio in enumerate(sentence.nep_audio.all()):
            with open(join(sent_dir, 'translation_{}.mp3'.format(j+1)), "wb") as nep:
                nep.write(audio.audio.file.read())
    tmp_dir2 = join('/tmp', str(uuid.uuid4()))
    os.mkdir(tmp_dir2)
    zipname = join(tmp_dir2, 'lesson.zip')
    os.chdir(tmp_dir)
    with zipfile.ZipFile(zipname, 'w') as zipf:
        zipdir('lesson', zipf)
    zipcontent = open(zipname, "rb").read()
    try:
        shutil.rmtree(tmp_dir)
    except:
        pass
    try:
        shutil.rmtree(tmp_dir2)
    except:
        pass
    response = HttpResponse(zipcontent, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=lesson.zip'
    return response




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
    lesson = get_object_or_404(Lesson, pk=lesson)
    context = {'lesson': lesson}
    if request.user != lesson.creator:
        raise Http404("Access denied")
    return render(request, 'everest/lesson/edit_lesson.html', context)


@login_required
@transaction.atomic
def create_sentence(request, lesson):
    lesson = get_object_or_404(Lesson, pk=lesson)
    context = {'lesson': lesson}
    if request.user != lesson.creator:
        raise Http404("Access denied")
    if request.method == 'POST':
        form = AddSentence(request.POST)
        if form.is_valid():
            sentence_text = form.cleaned_data['sentence']
            existing = Sentence.objects.filter(english=sentence_text).all()
            if existing:
                if lesson.sentences.filter(english=existing[0]):
                    context['error'] = 'This list already contains the sentence: '+sentence_text
                else:
                    lesson.sentences.add(existing[0])
                    lesson.save()
            else:
                new_sentence = Sentence(english=form.cleaned_data['sentence'], creator=request.user)
                new_sentence.save()
                lesson.sentences.add(new_sentence)
                lesson.save()
    return render(request, 'everest/lesson/sentence_table_del.html', context)


@login_required
@transaction.atomic
def add_sentence(request, sentence, lesson):
    sentence = get_object_or_404(Sentence, pk=sentence)
    lesson = get_object_or_404(Lesson, pk=lesson)
    if request.user != lesson.creator:
        raise Http404("Access denied")
    lesson.sentences.add(sentence)
    lesson.save()
    return render(request, 'everest/lesson/edit_lesson.html', {'lesson': lesson})
