from django.shortcuts import render
from django.http import HttpResponse
import json


def home(request):
    return render(request, 'everest/record.html', {})

def upload(request):
    print request.POST
    print request.FILES
    print request.GET
    #print request
    if request.POST:
        #print request.POST
        #print blob
        #print request.FILES
        pass
    to_json = {'yes': "hi"}
    return HttpResponse(json.dumps(to_json), content_type='application/json')
