import uuid
import contextlib
from shortuuid.django_fields import ShortUUIDField 
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
import random
from user_service.manager import UserManager


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_instructor = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    enable_two_factor_authentication = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_verified = True 
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
    @property
    def get_user_fullname(self):
        return f"{self.first_name} {self.last_name}"


class StudentProfile(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_service/student/profile_pictures/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        """Deletes old profile_picture when making an update to profile_picture"""
        with contextlib.suppress(Exception):
            old = StudentProfile.objects.get(id=self.id)
            if old.profile_picture != self.profile_picture:
                old.profile_picture.delete(save=False)
        super().save(*args, **kwargs)


class InstructorProfile(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_service/instructor/profile_pictures/', blank=True, null=True)
    total_students = models.PositiveIntegerField(default=0)
    reviews = models.PositiveIntegerField(default=0)
    linkedin = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Instructor Profiles'

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        """Deletes old profile_picture when making an update to profile_picture"""
        with contextlib.suppress(Exception):
            old = InstructorProfile.objects.get(id=self.id)
            if old.profile_picture != self.profile_picture:
                old.profile_picture.delete(save=False)
        super().save(*args, **kwargs)
        
class SMSCode(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='smscode')
    number = models.CharField(max_length=6, blank=False, null=False)

    def __str__(self):
        return f'{self.user.username}-{self.number}'

    def save(self, *args, **kwargs):
        verification_code = random.randint(100000, 999999)
        self.number = str(verification_code)

        super().save(*args, **kwargs)
