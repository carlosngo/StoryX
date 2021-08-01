from django.contrib import admin
from converter.models import Story, Scene, Event, DialogueEvent, ActionEvent, Entity, Character, Prop

class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

# Register your models here.
admin.site.register(Story, StoryAdmin)
admin.site.register(Scene)
admin.site.register(Event)
admin.site.register(DialogueEvent)
admin.site.register(ActionEvent)
admin.site.register(Entity)
admin.site.register(Character)
admin.site.register(Prop)