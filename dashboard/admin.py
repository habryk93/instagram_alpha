from django.contrib import admin
from dashboard.models import Picture

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    pass
