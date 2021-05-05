from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from converter.models import Story, Entity
from converter.forms import StoryForm
from converter.pipeline.element_extractor import ElementExtractor
from converter.pipeline.annotation_helper import AnnotationHelper
from converter.pipeline.screenplay_generator import ScreenplayGenerator

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
            text = story.text_file.open('r').read()
            # open(os.path.join(settings.MEDIA_ROOT, story.text_file.name), 'r').read()
            
            URL = "http://localhost:8001/api/coref-clusters"
            PARAMS = {'text':text}
            res = requests.get(url = URL, params = PARAMS)
            coref_json = res.json()

            element_extractor = ElementExtractor()
            element_extractor.extract_elements(story, text, coref_json)
            element_extractor.verify_elements()
            # characters = element_extractor.characters
            # props = element_extractor.props
            # events = element_extractor.events

            
            # for entity in list(Entity.objects.filter(story=story).order_by('reference_start')):
            #     print(f'{entity.reference_start}, {entity.reference_end}')
            
            # for character in characters:
            #     entity = character.entity
            #     entity.story = story
            #     entity.save()
            #     character.save()
            
            # for prop in props:
            #     entity = prop.entity
            #     entity.story = story
            #     entity.save()
            #     prop.save()

            # for evt in events:
            #     if type(evt) == ActionEvent:
            #         event = evt.event
            #     elif type(evt) == DialogueEvent:
            #         event = evt.event
            #     elif type(evt) == TransitionEvent:
            #         event = evt.action_event.event
            #     scene = event.scene
            #     scene.story = story
            #     scene.save()
            #     event.save()
            #     if type(evt) == TransitionEvent:
            #         evt.action_event.save()
            #     evt.save()
            return redirect('/converter/stories/')
    else:
        form = StoryForm()
    
    stories = Story.objects.all()

    return render(request, 'stories.html', {'stories': stories, 'form': form})

def annotate(request, id):
    story = get_object_or_404(Story, id=id)

    text = story.text_file.open('r').read()
    # text = open(os.path.join(settings.MEDIA_ROOT, story.text_file.name), 'r').read()
    
    annotation_helper = AnnotationHelper()
    annotation_helper.process(text)
    
    return render(request, 'annotate.html', {
        'title': story.title,
        'tokens': annotation_helper.tokens,
        'sentences': annotation_helper.sentences,
    })


def screenplay(request, id):
    story = get_object_or_404(Story, id=id)

    text = story.text_file.open('r').read()
    # text = open(os.path.join(settings.MEDIA_ROOT, story.text_file.name), 'r').read()

    screenplay_generator = ScreenplayGenerator(story, text)
    screenplay_generator.generate_screenplay()

    return render(request, 'index.html')


