from django.shortcuts import render, get_object_or_404
from haystack.query import SearchQuerySet
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from everest.forms import *


"""
Sentence Searches
"""


def search_sentences(request):
    context = {'base_description': 'All Sentences'}
    if add_query_to_context(request, context):
        clean_query = cleaned_query(context['query'])
        sqs = SearchQuerySet().models(Sentence).filter(content=clean_query)
        context['sentences'] = query_unique(sqs)
    else:
        context['sentences'] = Sentence.objects.all()
    context['search_url'] = reverse('search_sentences')
    return render(request, "everest/lists/list_of_sentences.html", context)


def search_needs_translation(request):
    context = {'base_description': 'Sentences Needing Translation'}
    if add_query_to_context(request, context):
        clean_query = cleaned_query(context['query'])
        sqs = SearchQuerySet().models(Sentence).filter(Q(translations__isnull=True, content=clean_query) | Q(nep_audio__isnull=True, content=clean_query))
        context['sentences'] = query_unique(sqs)
    else:
        context['sentences'] = Sentence.objects.filter(Q(translations__isnull=True) | Q(nep_audio__isnull=True))
    context['search_url'] = reverse('search_needs_translation')
    return render(request, "everest/lists/list_of_sentences.html", context)


def search_needs_engaudio(request):
    context = {'base_description': 'Sentences Needing English Audio'}
    if add_query_to_context(request, context):
        clean_query = cleaned_query(context['query'])
        sqs = SearchQuerySet().models(Sentence).filter(eng_audio__isnull=True, content=clean_query)
        context['sentences'] = query_unique(sqs)
    else:
        context['sentences'] = Sentence.objects.filter(eng_audio__isnull=True)
    context['search_url'] = reverse('search_needs_engaudio')
    return render(request, "everest/lists/list_of_sentences.html", context)


"""
Lesson Searches
"""


def search_lessons(request):
    context = {'base_description': 'All Lessons'}
    if add_query_to_context(request, context):
        clean_query = cleaned_query(context['query'])
        sqs = SearchQuerySet().models(Lesson).filter(content=clean_query)
        context['lessons'] = query_unique(sqs)
    else:
        context['lessons'] = Lesson.objects.all()
    context['search_url'] = reverse('search_lessons')
    return render(request, "everest/lists/list_of_lessons.html", context)


@login_required
def search_my_lessons(request):
    return search_user_lessons(request, request.user.username)


def search_user_lessons(request, username):
    user = get_object_or_404(User, username=username)
    context = {'base_description': 'Lessons by ' + user.username.capitalize()}
    if add_query_to_context(request, context):
        clean_query = cleaned_query(context['query'])
        sqs = SearchQuerySet().models(Lesson).filter(content=clean_query, creator=user)
        context['lessons'] = query_unique(sqs)
    else:
        context['lessons'] = user.lessons.all()
    context['search_url'] = reverse('search_user_lessons', kwargs={'username': username})
    return render(request, "everest/lists/list_of_lessons.html", context)


"""
User Searches
"""


def search_users(request):
    context = {'base_description': 'All Users'}
    if add_query_to_context(request, context):
        clean_query = cleaned_query(context['query'])
        sqs = SearchQuerySet().models(User).filter(content=clean_query)
        context['users'] = query_unique(sqs)
    else:
        context['users'] = User.objects.all()
    context['search_url'] = reverse('search_users')
    return render(request, "everest/lists/list_of_users.html", context)


"""
Search Utility Methods
"""


def cleaned_query(query):
    return SearchQuerySet().query.clean(query)


def query_unique(queryset):
    seen = set()
    for result in queryset:
        item = result.object
        if item not in seen:
            seen.add(item)
            yield item


def add_query_to_context(request, context):
    if request.GET:
        form = QueryForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query.strip() != '':
                context['query'] = query
                return True
    return False
