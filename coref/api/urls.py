from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('coref-clusters/', views.coref_clusters, name='coref-clusters'),
]