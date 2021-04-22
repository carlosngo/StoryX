from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stories/', views.stories, name='stories'),
    path('converter/start', views.start, name='start'),
    path('converter/main', views.main, name='main')
]