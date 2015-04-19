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


def search_user(request):
    context = {}
    if request.GET:
        form = QueryForm(request.GET)
        if form.is_valid():
            clean_query = SearchQuerySet().query.clean(form.cleaned_data['query'])
            sqs = SearchQuerySet().models(User).filter(content=clean_query)
            context['users'] = list(query_unique(sqs))
            context['query'] = request.GET['query']

    if 'users' not in context:
        context['users'] = User.objects.all()
    return render(request, "everest/lists/list_of_users.html", context)


def search_lesson(request):
    context = {}
    if request.GET:
        form = QueryForm(request.GET)
        if form.is_valid():
            clean_query = SearchQuerySet().query.clean(form.cleaned_data['query'])
            sqs = SearchQuerySet().models(Lesson).filter(content=clean_query)
            context['lessons'] = list(query_unique(sqs))
            context['query'] = request.GET['query']

    if 'lessons' not in context:
        context['lessons'] = Lesson.objects.all()
    return render(request, "everest/lists/list_of_lessons.html", context)


def search_sentence(request):
    context = {}
    if request.GET:
        form = QueryForm(request.GET)
        if form.is_valid():
            clean_query = SearchQuerySet().query.clean(form.cleaned_data['query'])
            sqs = SearchQuerySet().models(Sentence).filter(content=clean_query)
            context['sentences'] = list(query_unique(sqs))
            context['query'] = request.GET['query']

    if 'sentences' not in context:
        context['sentences'] = Sentence.objects.all()
    return render(request, "everest/lists/list_of_sentences.html", context)