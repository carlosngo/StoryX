from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stories/', views.stories, name='stories'),
    path('start/', views.start, name='start'),
    path('main/', views.main, name='main'),
    path('stories/<uuid:id>/annotate/', views.annotate, name='annotate'),
]