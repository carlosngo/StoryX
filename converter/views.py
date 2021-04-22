# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# from django.conf import settings

# from converter.models import Story
# from converter.forms import StoryForm
# from converter.pipeline.element_extractor import ElementExtractor
# from converter.pipeline.annotation_helper import AnnotationHelper

# import requests
# import os
# from django.views import generic

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from converter.models import Story
from converter.forms import StoryForm
from converter.pipeline.element_extractor import ElementExtractor
from converter.pipeline.annotation_helper import AnnotationHelper

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

def start(request):
    return render(request, 'start.html')

def main(request):
    return render(request, 'main.html')

def annotate(request, id):
    story = get_object_or_404(Story, id=id)

    text = open(os.path.join(settings.MEDIA_ROOT, story.text_file.name), 'r').read()
    
    annotation_helper = AnnotationHelper()
    annotation_helper.process(text)
    
    return render(request, 'annotate.html', {
        'title': story.title,
        'tokens': annotation_helper.tokens,
        'sentences': annotation_helper.sentences,
    })
