from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('start/', views.start, name='start'),
    path('main/', views.main, name='main'),
    path('stories/', views.stories, name='stories'),
    path('stories/<uuid:id>/annotate/', views.annotate, name='annotate'),
]