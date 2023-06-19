from django.contrib import admin

from .models import User, StudentProfile, InstructorProfile, SMSCode, InstructorSkill, SkillCertification



@admin.register(InstructorSkill)
class InstructorSkillAdmin(admin.ModelAdmin):
    list_display = ["instructor", "skill_name", "skill_level"]
    list_filter = ["instructor", "skill_level"]
    

@admin.register(SkillCertification)
class SkillCertificationAdmin(admin.ModelAdmin):
    list_display = ["skill", "certification_name", "certification_date"]
    list_filter = ["skill"]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'phone_number', 'address', 'city', 'state', 'country')
    search_fields = ('user__email', 'phone_number', 'city', 'state', 'country')
    list_filter = ('gender', 'country')

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender', 'phone_number', 'address', 'city', 'state', 'country', 'total_students', 'reviews', 'linkedin')
    search_fields = ('user__email', 'phone_number', 'city', 'state', 'country', 'linkedin')
    list_filter = ('gender', 'country')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_instructor']
    list_filter = ['is_instructor', 'created_at', 'is_verified']
    search_fields = ['email', 'first_name', 'last_name']


admin.site.register(SMSCode)
