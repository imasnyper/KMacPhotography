from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from project.serializers import UserSerializer, ProjectSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
import io
from base64 import b64encode
from io import BytesIO
from zipfile import ZipFile
from django.http import HttpResponse

from project.models import Project
from photo.models import Photo

def project_photos(request, *args, **kwargs):
    project_title = kwargs["project_title"]
    project = Project.objects.get(title=project_title)
    photos = project.photo_set.all()
    photo_tuples = []

    for photo in photos:
        image = photo.photo.storage.open(photo.photo.name, 'rb')
        bytes = b64encode(image.read()).decode()
        photo_tuples.append((photo.photo.name, bytes))
        image.close()

    context = {'photos': photo_tuples}

    return render(request, 'project/project_photos.html', context=context)


def download(request, *args, **kwargs):
    # https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html
    project_title = kwargs["project_title"]
    project = Project.objects.get(title=project_title)
    photos = project.photo_set.all()
    in_memory = BytesIO()
    zip = ZipFile(in_memory, "a")

    for photo in photos:
        image = photo.photo.storage.open(photo.photo.name, 'rb')
        bytes = image.read()
        zip.writestr(photo.photo.name, bytes)
        image.close()

    for file in zip.filelist:
        file.create_system = 0

    zip.close()

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = f"attachment; filename={project.title}-photos.zip"

    in_memory.seek(0)

    response.write(in_memory.read())

    return response

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        photos = request.data.pop('photos')
        photos = [{"photo": p} for p in photos]
        data = {"title": request.data["title"], "email_address": request.data["email_address"], "photos": photos}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #def perform_create(self, serializer):
    #    try:
    #        project = Project.objects.get(
    #            title=serializer.validated_data["title"],
    #            email_address=serializer.validated_data["email_address"]
    #        )
    #        serializer = ProjectSerializer(project)
    #        #serializer.save()
    #    except Project.DoesNotExist:
    #        project = serializer.save()

    #    photos = self.request.data.getlist("photos")
    #    for photo in photos:
    #        Photo.objects.create(project=project, photo=photo)
    #    return project