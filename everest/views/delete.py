from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse

from everest.forms import *


@login_required
@transaction.atomic
def del_translation(request, translation):
    was_deleted = False
    translation = get_object_or_404(Translation, id=translation)
    sentence = translation.sentence
    if request.method == 'POST' and request.user == translation.creator:
        translation.delete()
        was_deleted = cleanup(sentence)
    if was_deleted:
        return redirect(reverse('search_sentences'))
    context = {'sentence': sentence}
    return render(request, 'everest/sentence/sentence.html', context)


@login_required
@transaction.atomic
def del_englishaudio(request, audio):
    was_deleted = False
    audio = get_object_or_404(EnglishAudio, id=audio)
    sentence = audio.sentence
    if request.method == 'POST' and request.user == audio.creator:
        audio.delete()
        was_deleted = cleanup(sentence)

    if was_deleted:
        return redirect(reverse('search_sentences'))
    context = {'sentence': sentence}
    return render(request, 'everest/sentence/sentence.html', context)


@login_required
@transaction.atomic
def del_nepaliaudio(request, audio):
    was_deleted = False
    audio = get_object_or_404(NepaliAudio, id=audio)
    sentence = audio.sentence
    if request.method == 'POST' and request.user == audio.creator:
        audio.delete()
        was_deleted = cleanup(sentence)

    if was_deleted:
        return redirect(reverse('search_sentences'))
    context = {'sentence': sentence}
    return render(request, 'everest/sentence/sentence.html', context)

"""
Edit Lesson View Deletions
"""


@login_required
@transaction.atomic
def del_sentence(request, sentence, lesson):
    sentence = get_object_or_404(Sentence, id=sentence)
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.method == 'POST' and request.user == lesson.creator:
        lesson.sentences.remove(sentence)
        lesson.save()
        cleanup(sentence)
    context = {'lesson': lesson}
    return render(request, 'everest/lesson/sentence_table_del.html', context)


@login_required
@transaction.atomic
def del_lesson(request, lesson):
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.method == 'POST' and request.user == lesson.creator:
        to_clean = list(lesson.sentences.all())
        lesson.delete()
        for sentence in to_clean:
            cleanup(sentence)

    return redirect(reverse('search_my_lessons'))


# returns True if deleted sentence
def cleanup(sentence):
    if sentence.translations.all() or sentence.eng_audio.all() or sentence.nep_audio.all() or sentence.lessons.all():
        return False
    sentence.delete()
    return True

