from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from api.coref_resolver import CorefResolver

# Create your views here.
def index(request):
    return render(request, 'index.html')

def coref_clusters(request):
    coref_resolver = CorefResolver()
    if request.method == 'GET':
        if 'text' in request.GET and request.GET['text']:
            text = request.GET['text']
            return JsonResponse(coref_resolver.resolve_coreferences(text))
    return HttpBadRequest()



    