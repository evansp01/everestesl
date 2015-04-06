from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'everest/index.html', {})

def translate(request):
    context = {}
    snt = request.GET.get('s')   # ADD ERROR-CHECKING
    sentence = Sentence.objects.get(id=snt)
    context['sentence'] = sentence
    context['lessons'] = Lesson.objects.filter(sentences=sentence)
    return render(request, 'everest/sentence.html', context)


def need_translation(request):
    return render(request, 'everest/list_of_lessons.html', {})

def need_audio(request):
    return render(request, 'everest/list_of_lessons.html', {})

def profile(request):
    return render(request, 'everest/profile.html', {})
