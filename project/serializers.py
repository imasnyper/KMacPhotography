from django.contrib.auth.models import User
from rest_framework import serializers

from project.models import Project

from photo.models import Photo
from photo.serializers import PhotoSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(source="photo_set", many=True)

    class Meta:
        model = Project
        fields = ["title", "email_address", "photos"]

    def create(self, validated_data):
        photo_data = validated_data.pop('photo_set')
        photo_data = [dict(x)['photo'] for x in photo_data]
        project, created = Project.objects.get_or_create(**validated_data)
        for photo in photo_data:
            print(dir(photo))
            Photo.objects.create(project=project, photo=photo)
        return project