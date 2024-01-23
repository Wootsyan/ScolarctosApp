from django.contrib import admin

from .models import File

class FileAdmin(admin.ModelAdmin):
    model = File

    list_display = ('name', 'path')

admin.site.register(File, FileAdmin)