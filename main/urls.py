from django.urls import path

from . import views

urlpatterns = [
    path('menus/', views.menus, name='menus'),
    path('request', views.on_request, name='request'),
    path('apps', views.apps, name='apps'),
    path('open', views.open, name='open'),
    path('network', views.network, name='network'),
    path('webpage', views.webpage, name='webpage'),
]