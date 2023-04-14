from django.contrib import admin
from .models import Tag, TagModule, Module


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(TagModule)
class TagModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag', 'module']
    list_filter = ['tag', 'module']
    search_fields = ['tag__name', 'module__name']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course', 'created_at']
    list_filter = ['course']
    search_fields = ['name', 'description']
    autocomplete_fields = ['tags']
