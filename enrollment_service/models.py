from shortuuid.django_fields import ShortUUIDField 
from django.db import models
from user_service.models import StudentProfile
from course_service.models import Course

# Create your models here.

class Enrollment(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrolled_student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_course')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.student} enrolled for {self.course}"


class Payment(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False )
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='enrollment')
    amount = models.FloatField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    checkout_id = models.CharField(max_length=500)
    payment_date = models.DateTimeField(auto_now_add=True)