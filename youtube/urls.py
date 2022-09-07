from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video', views.video, name='video'),
    path('video_preview', views.video_preview, name='video_preview'),
]