from django.urls import path

from . import views

urlpatterns = [
    path('menus/', views.menus, name='menus'),
    path('request', views.on_request, name='request'),
]