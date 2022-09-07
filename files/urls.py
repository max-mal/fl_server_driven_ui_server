from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('open', views.open_path, name='open_path'),
    path('feh', views.open_feh, name='open_feh'),
]