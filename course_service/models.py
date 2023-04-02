from django.db import models
from shortuuid.django_fields import ShortUUIDField 
from user_service.models import InstructorProfile
from django.core.validators import MinValueValidator, MaxValueValidator
import contextlib
from django.conf import settings 
# Create your models here.

class Course(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    cover_image = models.ImageField(upload_to='course_service/courses/', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name="instructor", null=True)
    difficulty = models.PositiveIntegerField(
                                             validators=[
                                                         MinValueValidator(0), 
                                                         MaxValueValidator(5)
                                                        ], default=0
                                             )
    prerequisites = models.TextField(null=True, blank=True)
    requirements = models.TextField(null=True, blank=True)
    is_certified = models.BooleanField(default=False)
    reviews = models.PositiveIntegerField(validators=[
                                                      MinValueValidator(0), 
                                                      MaxValueValidator(5)
                                                     ], default=0
                                          )
    average_rating = models.FloatField(default=0)
    price = models.FloatField(null=True, blank=True)
    duration = models.CharField(max_length=30, null=True, blank=True)
    is_available = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("price",)
        
    @property
    def get_instructor_fullname(self):
        return f"{self.instructor.user.first_name} {self.instructor.user.last_name}"
        
    def __str__(self):
        return f"Course: {self.name} by {self.get_instructor_fullname}"
    
    def save(self, *args, **kwargs):
        """Deletes old cover_image when making an update to cover_image"""
        with contextlib.suppress(Exception):
            old = Course.objects.get(id=self.id)
            if old.cover_image != self.cover_image:
                old.cover_image.delete(save=False)
        super().save(*args, **kwargs)
    
    
class Review(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField(validators=[
                                                     MinValueValidator(0), 
                                                     MaxValueValidator(5)
                                                    ]
                                        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "course")
        
    def __str__(self):
        return f"Comment by {self.user.email} on {self.course.name}"
    
    
    