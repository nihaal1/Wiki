from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("wiki", views.index, name="index"),
    path("wiki/<str:name>", views.get, name="get")
    
]
