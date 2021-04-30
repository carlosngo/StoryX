from django import forms
from converter.models import Story

class StoryForm(forms.Form):
    title_field = forms.CharField(
        label='Title'
    )
    author_field = forms.CharField(
        label='Author'
    )
    file_field = forms.FileField(
        label='Select text file',
        help_text='max. 42 megabytes'
    )

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title', 'author', 'text_file')
