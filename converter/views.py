from django.shortcuts import render, redirect
from django.http import HttpResponse

from converter.models import Story
from converter.forms import StoryForm

# Create your views here.

def index(request):
    return HttpResponse("Hello World!")

def stories(request):
    # Handle file upload
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save()
            return redirect('/converter/stories/')
    else:
        form = StoryForm()
    
    stories = Story.objects.all()

    return render(request, 'stories.html', {'stories': stories, 'form': form})

