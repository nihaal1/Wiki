from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.pages, name="pages"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random_page",views.random_page, name="random_page"),
    
    
]
