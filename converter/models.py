import os
from django.db import models
import uuid

# Create your models here.

class Story(models.Model):
    def update_filename(instance, filename):
        path = "stories/"
        filename = instance.title.replace(' ', '-').lower()
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

class Entity(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    story = models.ForeignKey(
        Story, 
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
        on_delete=models.CASCADE
    )
    character = models.ManyToManyField(Character)
    prop = models.ManyToManyField(Prop)
    event_number = models.IntegerField()
    actor_start = models.IntegerField()
    actor_end = models.IntegerField()
    sentence_start = models.IntegerField()
    sentence_end = models.IntegerField()

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
    prop = models.ManyToManyField(Prop)
    verb = models.IntegerField()


class TransitionEvent(models.Model):
    action_event = models.OneToOneField(
        ActionEvent,
        on_delete=models.CASCADE,
        primary_key=True
    )

