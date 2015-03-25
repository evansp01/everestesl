from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'everest/index.html', {})

def need_translation(request):
    return render(request, 'everest/index.html', {})

def need_audio(request):
    return render(request, 'everest/index.html', {})

def profile(request):
    return render(request, 'everest/index.html', {})