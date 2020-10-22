from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=64)
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"{self.title}"