import os
from django.db import models

# Create your models here.

class Story(models.Model):
    def update_filename(instance, filename):
        path = "stories/"
        filename = instance.title.replace(' ', '-').lower()
        format = filename + '.txt'
        return os.path.join(path, format)

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    text_file = models.FileField(upload_to=update_filename, null=True)

