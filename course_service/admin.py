from django.contrib import admin
from .models import (
    Course, 
    Review, 
    Tag, 
    TagModule, 
    Module, 
    Lesson, 
    InstructorSkill, 
    SkillCertification,
    Quiz
)
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",  "difficulty", "is_available", "updated_at")
    list_filter = ( "difficulty", "is_available", "is_certified")
    search_fields = ( "name",)
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "updated_at")
    list_filter = ("user", "course")
    

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


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'module', 'created_at']
    list_filter = ['module']
    search_fields = ['name', 'description']
    
    
@admin.register(InstructorSkill)
class InstructorSkillAdmin(admin.ModelAdmin):
    list_display = ["instructor", "skill_name", "skill_level"]
    list_filter = ["instructor", "skill_level"]
    

@admin.register(SkillCertification)
class SkillCertificationAdmin(admin.ModelAdmin):
    list_display = ["skill", "certification_name", "certification_date"]
    list_filter = ["skill"]
    
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["name", "updated_at"]
    list_filter = ["updated_at", "created_at"]