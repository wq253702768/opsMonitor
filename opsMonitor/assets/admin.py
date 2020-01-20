from django.contrib import admin
from assets import models


# Register your models here.

class AssetsAdmin(admin.ModelAdmin):
    list_display = ['ip', 'username', 'password', 'rsa_key','env']


class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'component_type', 'memo']


admin.site.register(models.Assets, AssetsAdmin)
admin.site.register(models.Component, ComponentAdmin)
