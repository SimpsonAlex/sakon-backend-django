from django.contrib import admin
from .models import Client, Visit, ImageUrls

admin.site.register(Visit)
admin.site.register(Client)
admin.site.register(ImageUrls)
# Register your models here.
