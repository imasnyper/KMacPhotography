from rest_framework import serializers

from project.models import Project

from photo.models import Photo

class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = "__all__"
        depth = 1

    #def create(self, validated_data):
    #    project, created = Project.objects.get_or_create(title=validated_data['project']['title'], email_address=validated_data['project']['email_address'])
    #    photo = Photo.objects.create(project=project, photo=validated_data['photo'])
    #    return photo