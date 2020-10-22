"""
Definition of urls for KMacPhotography.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin

from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from project.views import UserViewSet, ProjectViewSet
from photo.views import PhotoViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'photos', PhotoViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('photos/', include('photo.urls')),
    path('projects/', include('project.urls')),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
