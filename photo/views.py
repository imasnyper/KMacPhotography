from django.shortcuts import render
import io
from base64 import b64encode
from io import BytesIO
from zipfile import ZipFile
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from project.models import Project
from project.serializers import ProjectSerializer

from photo.models import Photo
from photo.serializers import PhotoSerializer

import PIL.Image as Image


# Create your views here.
def photos(request):
    photos = Photo.objects.all()
    photo_tuples = []

    for photo in photos:
        image = photo.photo.storage.open(photo.photo.name, 'rb')
        bytes = b64encode(image.read()).decode()
        photo_tuples.append((photo.photo.name, bytes))
        image.close()

    context = {'photos': photo_tuples}

    return render(request, 'photo/index.html', context=context)


def download(request):
    # https://chase-seibert.github.io/blog/2010/07/23/django-zip-files-create-dynamic-in-memory-archives-with-pythons-zipfile.html
    photos = Photo.objects.all()
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
    response["Content-Disposition"] = "attachment; filename=photos.zip"

    in_memory.seek(0)

    response.write(in_memory.read())

    return response


class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    #parser_classes = [MultiPartParser]

    #def create(self, request, *args, **kwargs):
    #    data = {
    #        "project": {
    #            "title": request.data["project"], 
    #            "email_address": request.data["email"]
    #        }, 
    #        "photo": request.data["photo"]
    #    }
    #    serializer = self.get_serializer(data=data)
    #    serializer.is_valid(raise_exception=True)
    #    self.perform_create(serializer)

    #    headers = self.get_success_headers(serializer.data)

    #    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
