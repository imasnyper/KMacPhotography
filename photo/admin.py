from django.contrib import admin
from photo.models import Photo
from django.contrib.admin import views
from photo.forms import PhotoForm
from django.shortcuts import redirect

class PhotoAdmin(admin.ModelAdmin):
    form = PhotoForm

    def add_view(self, request, form_url='', extra_context=None):
        if (request.method == "POST"):
            form = PhotoForm(request.POST, request.FILES)
            photos = request.FILES.getlist('photo')
            if form.is_valid():
                project = form.cleaned_data['project']
                for p in photos:
                    photo_instance = Photo.objects.create(project=project, photo=p)

            return redirect('admin:photo_photo_changelist')

        return super().add_view(request, form_url=form_url, extra_context=extra_context)



admin.site.register(Photo, PhotoAdmin)