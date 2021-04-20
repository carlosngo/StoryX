from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from converter.models import Story
from converter.forms import StoryForm
from converter.pipeline.element_extractor import ElementExtractor

import requests
import os


# Create your views here.

def index(request):
    return HttpResponse("Hello World!")

def stories(request):
    # Handle file upload
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save()
            text = open(os.path.join(settings.MEDIA_ROOT, story.text_file.name), 'r').read()
            
            URL = "http://localhost:8001/api/coref-clusters"
            PARAMS = {'text':text}
            res = requests.get(url = URL, params = PARAMS)
            coref_json = res.json()

            element_extractor = ElementExtractor()
            element_extractor.extract_elements(text, coref_json)

            return redirect('/converter/stories/')
    else:
        form = StoryForm()
    
    stories = Story.objects.all()

    return render(request, 'stories.html', {'stories': stories, 'form': form})

