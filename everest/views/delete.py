from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, get_object_or_404

from everest.forms import *


@login_required
@transaction.atomic
def del_translation(request, translation):
    deletedSentence = False
    translation = get_object_or_404(Translation, id=translation)
    sentence = translation.sentence
    if request.method == 'POST' and request.user == translation.creator:
        translation.delete()
        sentenceWasDeleted = cleanup(sentence)

    if sentenceWasDeleted:
        context = {'sentences': Sentence.objects.all()}
        return render(request, 'everest/general/list_of_sentences.html', context)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)


@login_required
@transaction.atomic
def del_englishaudio(request, audio):
    sentenceWasDeleted = False
    audio = get_object_or_404(EnglishAudio, id=audio)
    sentence = audio.sentence
    if request.method == 'POST' and request.user == audio.creator:
        audio.delete()
        sentenceWasDeleted = cleanup(sentence)

    if sentenceWasDeleted:
        context = {'sentences': Sentence.objects.all()}
        return render(request, 'everest/general/list_of_sentences.html', context)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)


@login_required
@transaction.atomic
def del_nepaliaudio(request, audio):
    sentenceWasDeleted = False
    audio = get_object_or_404(NepaliAudio, id=audio)
    sentence = audio.sentence
    if request.method == 'POST' and request.user == audio.creator:
        audio.delete()
        sentenceWasDeleted = cleanup(sentence)

    if sentenceWasDeleted:
        context = {'sentences': Sentence.objects.all()}
        return render(request, 'everest/general/list_of_sentences.html', context)
    context = {'sentence': sentence}
    return render(request, 'everest/sentence.html', context)


@login_required
@transaction.atomic
def del_sentence(request, sentence, lesson):
    sentenceWasDeleted = False
    sentence = get_object_or_404(Sentence, id=sentence)
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.method == 'POST' and request.user == lesson.creator:
        lesson.sentences.remove(sentence)
        sentenceWasDeleted = cleanup(sentence)

    if sentenceWasDeleted:
        context = {'sentences': Sentence.objects.all()}
        return render(request, 'everest/general/list_of_sentences.html', context)
    context = {'lesson': lesson}
    return render(request, 'everest/edit_lesson.html', context)


@login_required
@transaction.atomic
def del_lesson(request, lesson):
    sentenceWasDeleted = False
    lesson = get_object_or_404(Lesson, id=lesson)
    if request.method == 'POST' and request.user == lesson.creator:
        if lesson.sentences.count():
            for sentence in lesson.sentences.all():
                cleanup(sentence)
    lesson.delete()
    context = {'lessons': Lesson.objects.all()}
    return render(request, 'everest/general/list_of_lessons.html', context)


# returns True if deleted sentence
def cleanup(sentence):
    if (not sentence.translations.all() and
            not sentence.eng_audio.all() and
            not sentence.nep_audio.all()):
        sentence.delete()
        return True
    else:
        return False
