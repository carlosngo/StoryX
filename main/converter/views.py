from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.files import File

from converter.models import Story, Entity
from converter.forms import StoryForm
from converter.pipeline.element_extractor import ElementExtractor
from converter.pipeline.annotation_helper import AnnotationHelper
from converter.pipeline.screenplay_generator import ScreenplayGenerator
from converter.pipeline.extraction_evaluator import ExtractionEvaluator
from converter.pipeline.understanding_evaluator import UnderstandingEvaluator
from converter.pipeline.story_presenter import StoryPresenter

import requests
import os


# Create your views here.

def stories(request):
    # Handle file upload
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save()
            text = story.text_file.open('r').read()
            
            URL = "http://localhost:8001/api/coref-clusters"
            PARAMS = {'text':text}
            res = requests.get(url = URL, params = PARAMS)
            coref_json = res.json()

            element_extractor = ElementExtractor()
            element_extractor.extract_elements(story, text, coref_json)
            # element_extractor.verify_elements()
            return redirect(story.get_screenplay_url())
    else:
        form = StoryForm()
    
    stories = Story.objects.all()

    return render(request, 'stories.html', {'stories': stories, 'form': form})

def story_txt(request, id):
    story = get_object_or_404(Story, id=id)
    return HttpResponse(story.text_file.open('rb'), content_type='text/plain')

def annotate(request, id):
    story = get_object_or_404(Story, id=id)

    text = story.text_file.open('r').read()

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
    
    path_to_pdf = os.path.join(settings.SCREENPLAY_ROOT, story.get_filename() + '.pdf')
    screenplay_generator = ScreenplayGenerator(story, text)
    screenplay_generator.generate_screenplay()
    # if there is no pdf file yet, generate one
    # if not os.path.isfile(path_to_pdf): 
    #     screenplay_generator = ScreenplayGenerator(story, text)
    #     screenplay_generator.generate_screenplay()

    return render(request, 'screenplay.html', {
        'story_id': story.id, 
        'pdf_url': story.get_pdf_url() + '#toolbar=0&view=FitH'
    })

def screenplay_pdf_download(request, id):
    story = get_object_or_404(Story, id=id)
    path_to_pdf = os.path.join(settings.SCREENPLAY_ROOT, story.get_filename() + '.pdf')
    with open(path_to_pdf, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=' + story.get_filename() + '.pdf'
        return response

def screenplay_tex_download(request, id):
    story = get_object_or_404(Story, id=id)
    path_to_tex = os.path.join(settings.SCREENPLAY_ROOT, story.get_filename() + '.tex')
    with open(path_to_tex, 'rb') as tex_file:
        response = HttpResponse(tex_file.read(), content_type="application/tex")
        response['Content-Disposition'] = 'attachment; filename=' + story.get_filename() + '.tex'
        return response
    
@xframe_options_sameorigin
def screenplay_pdf(request, id):
    story = get_object_or_404(Story, id=id)
    path_to_pdf = os.path.join(settings.SCREENPLAY_ROOT, story.get_filename() + '.pdf')
    return FileResponse(open(path_to_pdf, 'rb'), content_type='application/pdf')


def evaluate(request, id):
    story = get_object_or_404(Story, id=id)

    story_presenter = StoryPresenter(story)
    story_presenter.process()

    try:
        extraction_evaluator = ExtractionEvaluator(story)
        extraction_evaluator.evaluate_extraction()
    except FileNotFoundError:
        return render(request, 'evaluate.html', {
            'story': story,
            'sentences': story_presenter.sentences,
            'has_annotation': False,
        })

    score_labels = ['Precision', 'Recall', 'F1 Score']

    return render(request, 'evaluate.html', {
        'story': story,
        'sentences': story_presenter.sentences,
        'dialogue_content_score': list(zip(score_labels, extraction_evaluator.dialogue_content_score)),
        'dialogue_speaker_score': list(zip(score_labels, extraction_evaluator.dialogue_speaker_score)),
        'character_score': list(zip(score_labels, extraction_evaluator.character_score)),
        'prop_score': list(zip(score_labels, extraction_evaluator.prop_score)),
        'action_score': list(zip(score_labels, extraction_evaluator.action_score)), 
        'transition_score': list(zip(score_labels, extraction_evaluator.transition_score)), 
        'has_annotation': True,
    })


def extraction_results(request):
    stories = Story.objects.all()
    dltk_titles = {
        "Gingerbread Man",
        "Little Red Hen",
        "Moon Maiden",
        "Stone Soup",
        "The Emperor's New Clothes",
        "Thumbelina",
        "Beauty and the Beast",
        "Cinderella",
        "Jack and the Beanstalk",
        "Little Red Riding Hood",
        "Sleeping Beauty",
        "The Little Mermaid",
        "The Three Little Pigs",
        "Aladdin and the Wonderful Lamp",
        "Frog Prince",
        "Hansel and Gretel",
        "Puss in Boots",
        "Rapunzel",
        "Rumpelstiltskin",
        "Snow White and the Seven Dwarves",
        "The Ugly Duckling",
        "Goldilocks and the Three Bears",
        "Marie and the Orange Fish",
        "Molly Murphy and the Scorched Leprechaun",
        "Sedna",
        "The Story of Arachne, the Weaver",
        "The Story of Icarus",
        "The Story of Medusa and Athena",
        "Theseus and the Minotaur",
        "The Story of Prometheus' Fire",
    }

    extraction_results = {
        "agg": {
            "Dialogue Content": [0, 0, 0],
            "Dialogue Speaker": [0, 0, 0],
            "Character": [0, 0, 0],
            "Prop": [0, 0, 0],
            "Action Line": [0, 0, 0],
            "Scene Transition": [0, 0, 0],
        },
        "corpus": {
            "dltk": {
                "stories": [],
                "agg": {
                    "Dialogue Content": [0, 0, 0],
                    "Dialogue Speaker": [0, 0, 0],
                    "Character": [0, 0, 0],
                    "Prop": [0, 0, 0],
                    "Action Line": [0, 0, 0],
                    "Scene Transition": [0, 0, 0],
                }
            },
            "main": {
                "stories": [],
                "agg": {
                    "Dialogue Content": [0, 0, 0],
                    "Dialogue Speaker": [0, 0, 0],
                    "Character": [0, 0, 0],
                    "Prop": [0, 0, 0],
                    "Action Line": [0, 0, 0],
                    "Scene Transition": [0, 0, 0],
                }
            }
        }

    }
    for story in stories:
        story_results = {
            "elements": {}
        }
        story_results["title"] = story.title

        try:
            extraction_evaluator = ExtractionEvaluator(story)
            extraction_evaluator.evaluate_extraction()
            story_results['elements']["Dialogue Content"] = extraction_evaluator.dialogue_content_score
            story_results['elements']["Dialogue Speaker"] = extraction_evaluator.dialogue_speaker_score
            story_results['elements']["Character"] = extraction_evaluator.character_score
            story_results['elements']["Prop"] = extraction_evaluator.prop_score
            story_results['elements']["Action Line"] = extraction_evaluator.action_score
            story_results['elements']["Scene Transition"] = extraction_evaluator.transition_score
        except FileNotFoundError:
            pass
        if story.title in dltk_titles:
            extraction_results["corpus"]['dltk']["stories"].append(story_results)
        else:
            extraction_results["corpus"]['main']["stories"].append(story_results)

        
    for corpus in extraction_results['corpus']:
        agg = {
            "Dialogue Content": [0, 0, 0],
            "Dialogue Speaker": [0, 0, 0],
            "Character": [0, 0, 0],
            "Prop": [0, 0, 0],
            "Action Line": [0, 0, 0],
            "Scene Transition": [0, 0, 0],
        }
        stories = extraction_results['corpus'][corpus]['stories']
        for element in agg:
            for i in range(3):
                for j in range(len(stories)):
                    try:
                        agg[element][i] += stories[j]['elements'][element][i]
                    except KeyError:
                        pass

                agg[element][i] /= len(stories)
            
        extraction_results['corpus'][corpus]['agg'] = agg
    agg = {
        "Dialogue Content": [0, 0, 0],
        "Dialogue Speaker": [0, 0, 0],
        "Character": [0, 0, 0],
        "Prop": [0, 0, 0],
        "Action Line": [0, 0, 0],
        "Scene Transition": [0, 0, 0],
    }
    
    for element in agg:
        for i in range(3):
            for corpus in extraction_results['corpus']:
                agg[element][i] += extraction_results['corpus'][corpus]['agg'][element][i]
            agg[element][i] /= 2
    total = [0.0, 0.0, 0.0]
    for i in range(3):
        for element in agg:
            total[i] += agg[element][i]
        total[i] /= len(agg)
    
        
    extraction_results['agg'] = agg
    extraction_results['total'] = total
    print(extraction_results)
    return render(request, 'extraction_results.html', {'extraction_results': extraction_results})

def understanding_results(request):
    understanding_evaluator = UnderstandingEvaluator()
    understanding_results = understanding_evaluator.evaluate_understanding()
    print(understanding_results['agg'])
    return render(request, "understanding_results.html", {
        "understanding_results": understanding_results,
    })

    
