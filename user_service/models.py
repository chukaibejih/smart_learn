import uuid
import contextlib
from shortuuid.django_fields import ShortUUIDField 
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import random
from user_service.manager import UserManager
from django.utils import timezone

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
            self.enable_two_factor_authentication = False
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
    @property
    def get_user_fullname(self):
        return f"{self.first_name} {self.last_name}"


class StudentProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        
        # Set the student ID to be the same as the user ID
        self.id = self.user.id
        super().save(*args, **kwargs)


class InstructorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        # Deletes old profile_picture when making an update to profile_picture
        with contextlib.suppress(Exception):
            old = InstructorProfile.objects.get(id=self.id)
            if old.profile_picture != self.profile_picture:
                old.profile_picture.delete(save=False)

        # Set the student ID to be the same as the user ID
        self.id = self.user.id
        super().save(*args, **kwargs)
        
class SMSCode(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='smscode')
    number = models.CharField(max_length=6, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name}-{self.number}'

    def save(self, *args, **kwargs):
        verification_code = random.randint(100000, 999999)
        self.number = str(verification_code)

        super().save(*args, **kwargs)
    
    def is_expired(self, expiration_minutes=10):
        expiration_time = self.created_at + timezone.timedelta(minutes=expiration_minutes)
        return timezone.now() >= expiration_time


class InstructorSkill(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="insructor_skill")
    skill_name = models.CharField(max_length=40, null=True, blank=True)
    skill_level = models.PositiveIntegerField(validators=[
                                                     MinValueValidator(0),
                                                     MaxValueValidator(10)
                                                    ]
                                                    )
    
    class Meta:
        ordering = ["-skill_level"]

    def __str__(self):
        return self.skill_name

class SkillCertification(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    skill = models.OneToOneField(InstructorSkill, on_delete=models.CASCADE, blank=True, null=True, related_name="skill_certification")
    certification_name = models.CharField(max_length=50)
    certification_date = models.DateField()
    certificate_file = models.ImageField(upload_to="user_service/instructor/certificates/", null=True, blank=True)

    class Meta:
        ordering = ("skill__instructor",)

    def __str__(self):
        return f"{self.certification_name} for {self.skill.skill_name} "

    def save(self, *args, **kwargs):
        """Deletes old cover_image when making an update to cover_image"""
        with contextlib.suppress(Exception):
            old = SkillCertification.objects.get(id=self.id)
            if old.certificate_file != self.certificate_file:
                old.certificate_file.delete(save=False)
        super().save(*args, **kwargs)
