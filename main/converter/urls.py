from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stories/', views.stories, name='stories'),
    path('stories/<uuid:id>/annotate/', views.annotate, name='annotate'),
    path('stories/<uuid:id>/screenplay/', views.screenplay, name='screenplay'),
]