import os
from django.db import models
import uuid

# Create your models here.

class Story(models.Model):
    def update_filename(instance, filename):
        path = "stories/"
        filename = instance.title
        # filename = instance.title.replace(' ', '-').lower()
        format = filename + '.txt'
        return os.path.join(path, format)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    text_file = models.FileField(
        upload_to=update_filename,
        null=True
    )
    
    def get_absolute_url(self):
        return "/converter/stories/%s" % self.id

    def get_evaluation_url(self):
        return "/converter/stories/%s/evaluate" % self.id
    def get_annotation_url(self):
        return "/converter/stories/%s/annotate" % self.id

    def get_screenplay_url(self):
        return "/converter/stories/%s/screenplay" % self.id

    def get_pdf_url(self):
        return "/converter/stories/%s/screenplay/pdf" % self.id

    def get_txt_url(self):
        return "/converter/stories/%s/txt" % self.id

    def get_filename(self):
        return os.path.splitext(os.path.basename(self.text_file.name))[0]

class Entity(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    story = models.ForeignKey(
        Story, 
        on_delete=models.CASCADE,
    )
    refers_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    reference_start = models.IntegerField()
    reference_end = models.IntegerField()

class Character(models.Model):
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        primary_key=True,
    )

class Prop(models.Model):
    entity = models.OneToOneField(
        Entity,
        on_delete=models.CASCADE,
        primary_key=True,
    )

class Scene(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE
    ) 
    scene_number = models.IntegerField()

class Event(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    scene = models.ForeignKey(
        Scene, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    characters = models.ManyToManyField(Character)
    props = models.ManyToManyField(Prop)
    event_number = models.IntegerField(blank=True, null=True)
    sentence_start = models.IntegerField()
    sentence_end = models.IntegerField()
    is_transition = models.BooleanField()

class DialogueEvent(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    content_start = models.IntegerField()
    content_end = models.IntegerField()

class ActionEvent(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # verb = models.IntegerField()
