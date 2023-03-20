from django.contrib import admin

from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_instructor']
    list_filter = ['is_instructor', 'created_at', 'is_verified']
    search_fields = ['email', 'first_name', 'last_name']
