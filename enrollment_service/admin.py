from django.contrib import admin
from .models import Enrollment, Payment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'course']
    list_filter = ['course', 'enrollment_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'enrollment', 'amount', 'is_paid']
    list_filter = ['enrollment', 'amount', 'is_paid']
