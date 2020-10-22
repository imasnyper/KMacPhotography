from django.urls import path

from photo import views

urlpatterns = [
    path("", views.photos),
    path("download/", views.download),
]
