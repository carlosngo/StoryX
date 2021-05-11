from django.urls import path

from . import views

urlpatterns = [
    path('stories/', views.stories, name='stories'),
    path('stories/<uuid:id>/txt/', views.story_txt, name='story_txt'),
    path('stories/<uuid:id>/annotate/', views.annotate, name='annotate'),
    path('stories/<uuid:id>/screenplay/', views.screenplay, name='screenplay'),
    path('stories/<uuid:id>/screenplay/pdf', views.screenplay_pdf, name='screenplay_pdf'),
    path('stories/<uuid:id>/screenplay/pdf/download', views.screenplay_pdf_download, name='screenplay_pdf_download'),
    path('stories/<uuid:id>/screenplay/tex/download', views.screenplay_tex_download, name='screenplay_tex_download'),
    path('stories/<uuid:id>/screenplay/tex/download', views.evaluate, name='evaluate'),
]