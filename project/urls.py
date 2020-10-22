from django.urls import path, include

from project.views import project_photos, download


urlpatterns = [
    path('<project_title>/', project_photos),
    path('<project_title>/download/', download),
]