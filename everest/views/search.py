from django.shortcuts import render, get_object_or_404
from haystack.query import SearchQuerySet

from everest.forms import *


def query_unique(queryset):
    seen = set()
    for result in queryset:
        item = result.object
        if item not in seen:
            seen.add(item)
            yield item


def search_user():
    pass


def search_lesson(request):
    context = {}
    if request.GET:
        form = QueryForm(request.GET)
        if form.is_valid():
            clean_query = SearchQuerySet().query.clean(form.cleaned_data['query'])
            sqs = SearchQuerySet().models(Lesson).filter(content=clean_query)
            context['lessons'] = list(query_unique(sqs))
            for item in context['lessons']:
                print item
    if 'lessons' not in context:
        context['lessons'] = Lesson.objects.all()

    return render(request, "everest/general/list_of_lessons.html", context)

def search_sentence():
    pass


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