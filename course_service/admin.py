from django.contrib import admin
from .models import Course
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",  "difficulty", "is_available", "updated_at")
    list_filter = ( "difficulty", "is_available", "is_certified")
    search_fields = ( "name",)
    
    
    