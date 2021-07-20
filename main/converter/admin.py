from django.contrib import admin
from converter.models import Story, Scene, Event, DialogueEvent, ActionEvent, Entity, Character, Prop

# Register your models here.
admin.site.register(Story)
admin.site.register(Scene)
admin.site.register(Event)
admin.site.register(DialogueEvent)
admin.site.register(ActionEvent)
admin.site.register(Entity)
admin.site.register(Character)
admin.site.register(Prop)