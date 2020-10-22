from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from project.models import Project
import os
from django.core.files.storage import default_storage
from django.conf import settings

def get_upload_path(instance, filename):
    return os.path.join(f"{instance.project.title}", filename)

class Photo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to=get_upload_path, width_field="width", height_field="height")
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.photo.name}"

    def __repr__(self):
        return f"{self.photo.name}"

@receiver(pre_delete)
def delete(sender, instance, **kwargs):
    if isinstance(instance, Photo):
        default_storage.delete(instance.photo.name)
    elif isinstance(instance, Project):
        photos = instance.photo_set.all()
        for photo in photos:
            default_storage.delete(photo.photo.name)
