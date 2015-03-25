from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'everest/index.html', {})

def add_list(request):
    return render(request, 'everest/index.html', {})

def user_lists(request):
    return render(request, 'everest/index.html', {})

def profile(request):
    return render(request, 'everest/index.html', {})
