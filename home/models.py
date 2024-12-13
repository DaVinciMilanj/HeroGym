from django.db import models
from django.utils.html import format_html


# Create your models here.

class Gallery(models.Model):
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery')

    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', self.image.url)
        return "No Image Available"

    image_preview.short_description = "Preview"
