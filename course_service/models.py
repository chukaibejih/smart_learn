from django.db import models
from shortuuid.django_fields import ShortUUIDField 
from user_service.models import InstructorProfile
from django.core.validators import MinValueValidator, MaxValueValidator
import contextlib
from django.conf import settings
from django.core.validators import FileExtensionValidator
# Create your models here.

class Course(models.Model):

    DIFFICULTY = (
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced")
    )

    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    cover_image = models.ImageField(upload_to='course_service/courses/', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE, related_name="instructor", null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, null=True, blank=True)
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
        ordering = ["price"]
        
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


class Tag(models.Model):
    # Represents a tag for a module
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Module(models.Model):
    # Represents a module in a course
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='module_service/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(Tag, through='TagModule', blank=True)


    class Meta:
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Delete old thumbnail when making an update to the thumbnail 
        with contextlib.suppress(Exception):
            old = Module.objects.get(id=self.id)
            if old.thumbnail != self.thumbnail:
                old.thumbnail.delete(save=False)
        super().save(*args, **kwargs)  


class Lesson(models.Model):
    # Represents a lesson in a module
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module')
    video_url = models.URLField(blank=True, null=True)
    lesson_video = models.FileField(upload_to='Lesson_material/videos/', validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])], blank=True, null=True)
    lesson_documents = models.FileField(upload_to='Lesson_material/documents/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])], blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    resources = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_document_type(self):
        ext = str(self.lesson_documents).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'
    

class TagModule(models.Model):
    # Represents the many-to-many relationship between tags and modules
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tag.name} - {self.module.name}"
      
    
class Review(models.Model):
    id = ShortUUIDField(primary_key=True, length=6, max_length=6, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review")
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
        ordering = ["updated_at"]
        
    def __str__(self):
        return f"Comment by {self.user.email} on {self.course.name}"


class Quiz(models.Model):
    id = ShortUUIDField(primary_key=True, max_length=6, length=6, editable=False)
    name = models.CharField(max_length=70)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="quizes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("updated_at",)
        verbose_name_plural = "Quizes"
    
    def __str__(self):
        return self.name 
    
    