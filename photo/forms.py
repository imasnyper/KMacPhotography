from django.forms import ModelForm, ClearableFileInput
from photo.models import Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['project', 'photo']
        widgets = {
            'photo': ClearableFileInput(attrs={'multiple': True})
        }
