from django.contrib import admin
from .models import *
# Register your models here.

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'description')
    readonly_fields = ('image_preview',)  # فقط نمایش پیش‌نمایش در فرم ویرایش


admin.site.register(Gallery,GalleryAdmin)